$(function () {
  $('.palette .widget').click(function () {
    var widget = $('.widgetPrototype', this);
    kiab.addWidget(widget);
  });
  $('.control', $('#details')).blur(function (e) {
    control = $(this);
    newData = control.contents()
    
    $.post('update', {
      update: control.id,
      detail: newData
    });
    this.name;
  });
  
  $('.widget .control')
});

kiab = {
  addWidget: function (widget) {
    var widget = widget.contents().clone();
    widget.id = $.uuid()
    widget.appendTo($('#details'));
    widget
    $('input', widget).animate({ 
      backgroundColor: '#afa'
    }, 30).animate({ 
      backgroundColor: '#fff'
    }, 3000);
  },
  scope: $.scope()
};
