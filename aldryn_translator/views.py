import json
import uuid

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import FormView

from core import get_quote, get_order, copy_page, insert_response, prepare_data, prepare_order_data
from models import TranslationRequest, TranslationResponse
from forms import AddTranslationForm, SelectPluginsByTypeForm
from helpers import check_stage, log


class AddTranslationView(FormView):
    template_name = 'aldryn_translator/add_translation.html'
    form_class = AddTranslationForm
    trans_pk = ''

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(AddTranslationView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('admin:select_plugins_by_type', kwargs={'pk': self.trans_pk})

    def form_valid(self, form):
        f = form.save(commit=False)
        f.from_lang = form.cleaned_data['from_lang']
        f.to_lang = form.cleaned_data['to_lang']
        f.provider = form.cleaned_data['provider']
        f.copy_content = form.cleaned_data['copy_content']
        # Always true atm (for ease of use)
        # f.all_pages = form.cleaned_data['all_pages']
        f.all_pages = True
        # Not Active yet
        # f.all_stacks = form.cleaned_data['all_stacks']
        f.save()

        self.trans_pk = f.pk

        return super(AddTranslationView, self).form_valid(form)

@staff_member_required
def select_plugins_by_type_view(request, pk):
    t = TranslationRequest.objects.get(pk=pk)
    check_stage(t.status, 'draft')

    data = prepare_data(t, t.from_lang, t.to_lang)
    plugins = dict()
    for p in data['Groups']:
        if p['Context'] not in plugins:
            plugins[p['Context']] = 0
        plugins[p['Context']] += 1

    form = SelectPluginsByTypeForm(request.POST or None, plugins=plugins)

    if request.POST:
        if form.is_valid():
            t.order_selection = form.cleaned_data['plugins']
            t.status = 'selected_content'
            t.save()
            return redirect(reverse('admin:get_quote', kwargs={'pk': t.pk}))
    else:
        return render_to_response(
            'aldryn_translator/select_plugins_by_type.html',
            {'form': form}, context_instance=RequestContext(request)
        )

@staff_member_required
def select_plugins_by_id_view(request, pk):
    t = TranslationRequest.objects.get(pk=pk)
    check_stage(t.status, 'draft')

    if request.method == 'POST':
        raise NotImplementedError()
        t.status = 'selected_content'
        t.save()

    else:
        data = prepare_data(t, t.from_lang, t.to_lang)
        return render_to_response(
            'aldryn_translator/select_plugins_by_id.html', {'groups': data['Groups']},
            context_instance=RequestContext(request))

@staff_member_required
def get_quote_view(request, pk):
    t = TranslationRequest.objects.get(pk=pk)
    check_stage(t.status, 'selected_content')

    if request.method == 'POST':
        if request.POST.get('opt'):
            t.order_choice = request.POST.get('opt')  # TODO: possible security issue?
            t.status = 'selected_quote'
            t.save()
            return HttpResponseRedirect(reverse('admin:order', kwargs={'pk': pk}))

    else:
        quote = get_quote(t.provider, data=prepare_data(t, t.from_lang, t.to_lang))

        if t.provider == 'supertext':
            res = json.loads(quote)
            return render_to_response(
                'aldryn_translator/quote.html', {'res': res},
                context_instance=RequestContext(request))

        else:
            raise NotImplementedError()

@staff_member_required
def order_view(request, pk):
    t = TranslationRequest.objects.get(pk=pk)
    check_stage(t.status, 'selected_quote')

    t.reference = "%s-%s" % (str(pk), str(uuid.uuid4()))
    t.order_name = "Aldryn Translator Order"

    # COPY OLD LANG PAGE TREE TO NEW ONE
    if t.copy_content:
        copy_page(t.from_lang, t.to_lang)

    data = prepare_data(t, t.from_lang, t.to_lang, plugin_source_lang=t.to_lang)
    data.update(prepare_order_data(request, t))
    order = json.loads(get_order(t.provider, data))

    # DEBUG: log(data)
    t.sent_content = json.dumps(data)
    t.status = 'requested'
    t.save()

    # TODO: save other stuff from response to model (deadline, price, more?)

    if t.provider == 'supertext':
        return render_to_response(
            'aldryn_translator/confirmation.html', {'r': order},
            context_instance=RequestContext(request))

    else:
        raise NotImplementedError()


@csrf_exempt
def process_response(request):
    response = json.loads(request.body)

    trans_resp = TranslationResponse()
    trans_resp.received_content = response

    try:
        pk = response['ReferenceData'].partition("-")[0]
        trans_req = TranslationRequest.objects.get(pk=pk)
    except TranslationRequest.DoesNotExist:
        trans_resp.debug_info = "Translation Request with this PK could not be found"
        trans_resp.valid = False
        trans_resp.save()
        return HttpResponse(status=500, content="fail (1)")

    if not trans_req.status == 'requested':
        trans_resp.debug_info = "Translation Request's status is not valid for this step."
        trans_resp.valid = False
        trans_resp.save()
        return HttpResponse(status=500, content="fail (2)")

    if not trans_req.reference == response['ReferenceData']:
        trans_resp.debug_info = "Translation Request's ReferenceData does not match the one from the response!"
        trans_resp.valid = False
        trans_resp.save()
        trans_req.status = 'failed'
        return HttpResponse(status=500, content="fail (3)")

    trans_resp.valid = True
    trans_resp.request = trans_req
    trans_req.status = 'done'
    trans_resp.save()

    insert_response(trans_req.provider, response)

    return HttpResponse()
