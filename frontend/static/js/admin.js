const alertPlaceholder = document.getElementById('liveAlertPlaceholder');

const appendAlert = (message, type, url) => {
  const wrapper = document.createElement('div');
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    `   <a href="${url}" class="btn btn-danger">Eliminar Cabaña</a>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('');

  alertPlaceholder.append(wrapper);
};

document.querySelectorAll('.liveAlertBtn').forEach(button => {
  button.addEventListener('click', () => {
    var cabinName = button.getAttribute('data-nombre');
    var url = button.getAttribute('data-url');
    appendAlert(`Seguro desea eliminar la cabaña de nombre ${cabinName}?`, 'danger', url);
  });
});
