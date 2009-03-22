jQuery.query = function (query) {
  var tokens = query.toLowerCase().split(/\s+/g);  

  var bitmap = $.map(new Array(index[0].length), function (value, index) { return index; });
  $.each(tokens, function (i, token) {
    var hits = [];
    if (token) {
      $.each(index[1], function (key, value) {
        if (key.substr(0, token.length) === token) {
          hits = hits.concat(value);
        }
      });
    }    
    hits = $.unique(hits);
    bitmap = $.grep(bitmap, function (val, _) {
      return $.inArray(val, hits) >= 0;
    });

  });
  
  return $.map(bitmap, function(v, i) {
    return [index[0][v]];
  });
}

jQuery(function () {
  index = eval($('script.combo_index').text());

  list = $('<ul></ul>');    
  var currentQuery = '';
  var results = [];
  var selected = -1;
  
  $('input.combo_source').change(function (e) {
    list.hide();
    if (selected === -1 && results.length > 0) {
      selected = 0;
      $(this).val(results[selected][1]);
    }
    $('input.combo_target').val(results[selected][0]);
  });
  
  $('input.combo_source').keypress(function (e) {
    if (selected !== -1) {
      $($('li', list)[selected]).addClass('inactive_');
      $($('li', list)[selected]).removeClass('active_');
    }
        
    if (e.keyCode === 38) { //up
      selected -= 1;      
    } else if (e.keyCode === 40) { //down
      selected += 1;
    } else {
      return;
    }
    
    if (selected < 0) {
      selected = results.length - 1;
    } else if (selected >= results.length) {
      selected = -1;
    }
    
    if (selected === -1) {
      $(this).val(currentQuery);
    } else {
      $(this).val(results[selected][1]);
      $($('li', list)[selected]).removeClass('inactive_');
      $($('li', list)[selected]).addClass('active_');
    }      
  });
  
  $('input.combo_source').keyup(function (e) {
    if (e.keyCode === 38 || e.keyCode === 40) {
      return;
    }    
    currentQuery = $(this).val();
    results = $.query(currentQuery).slice(0, 10);
    selected = -1;
    
    list.hide().empty().addClass('combo_style');
    $.each(results, function (key, value) {
      list.append($('<li class="inactive_">'+value[1]+'</li>'));
    });
    if (results.length > 0) {
      list.show();
    }
    $('#id_agent').after(list);
    list[0].style.top = list.parent().position().top+30+"px";
    list[0].style.left = list.parent().position().left+30+"px";

  });
});

$=jQuery
