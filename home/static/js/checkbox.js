/* Обработчик клика на чекбоксах */
$('input').on('input', function() {
    let aChecked = [];
    $('input[type="checkbox"]:checked').each(function() { aChecked.push($(this).getPath()); });
    localStorage.setItem('CheckboxChecked', aChecked.join(';'));
    localStorage.setItem('PasswordLength', $('#height_opt').val());
  });
  
  /* Установка состояний чекбоксов, после загрузки страницы */
  $(document).ready(function() {
    if (localStorage.getItem('CheckboxChecked')) {
      let aChecked = localStorage.getItem('CheckboxChecked').split(';');
      $('input[type="checkbox"]').prop('checked', false);
      aChecked.forEach(function(str) { $(str).prop('checked', true); });
    }
    if (localStorage.getItem('PasswordLength')) {
      $('#height_opt').val(localStorage.getItem('PasswordLength'));
    }
  });
  
  /************************************************************
   * Функция для jQ, возвращающая уникальный селектор элемента *
   * Источник: https://stackoverflow.com/a/26762730/10179415   *
   ************************************************************/
  jQuery.fn.extend({
    getPath: function() {
      let pathes = [];
      this.each(function(index, element) {
        let path, $node = jQuery(element);
        while ($node.length) {
          let realNode = $node.get(0), name = realNode.localName;
          if (!name) { break; }
          name = name.toLowerCase();
          let parent = $node.parent();
          let sameTagSiblings = parent.children(name);
          if (sameTagSiblings.length > 1) {
            let allSiblings = parent.children();
            let index = allSiblings.index(realNode) + 1;
            if (index > 0) { name += ':nth-child(' + index + ')'; }
          }
          path = name + (path ? '>' + path : '');
          $node = parent;
        }
        pathes.push(path);
      });
      return pathes.join(',');
    }
  });
  
function clearAll() {
    localStorage.clear();
    checkStorage();
}