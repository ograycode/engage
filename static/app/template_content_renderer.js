$(document).ready(() => {
  const TEMPLATE_FORM = '#id_content';
  const TEMPLATE_PREVIEW = '#template-content-preview';
  const PREVIEW_DATA = '#id_preview_data';

  const SUBJECT_FORM = '#id_subject';
  const SUBJECT_PREVIEW = '#subject-content-preview';

  const updatePreview = () => {
    const update = (formId, previewId, dataId, isHtml) => {
      const source = $(formId).val();
      const template = Handlebars.compile(source);
      const context = JSON.parse($(dataId).val());
      const html = template(context);
      if (isHtml) {
        $(previewId).contents().find('html').html(html);
      } else {
        $(previewId).html(html);
      }
    };

    update(TEMPLATE_FORM, TEMPLATE_PREVIEW, PREVIEW_DATA, true);
    update(SUBJECT_FORM, SUBJECT_PREVIEW, PREVIEW_DATA, false);
  };

  updatePreview();

  $(TEMPLATE_FORM).on('keyup', function() {
    updatePreview();
  });

  const createCodeMirror = (textAreaId, modeOption) => {
    const options = {
      lineNumbers: true,
      mode: modeOption
    };
    CodeMirror.fromTextArea($(textAreaId)[0], options).on('change', (editor) => {
      $(textAreaId).val(editor.getValue());
      updatePreview();
    });
  };

  createCodeMirror(PREVIEW_DATA, {name: 'javascript', json: true});
  createCodeMirror(TEMPLATE_FORM, 'text/html');
  createCodeMirror(SUBJECT_FORM, 'text/html');

});
