$(function () {
  $('.palette .widget').click(function () {
    var widget = $('.widgetPrototype .detailTable', this);
    kiab.addWidget(widget);
  });
  $('.control', $('#details')).blur(kiab.sendUpdate);
  $('.name', $('#details')).blur(kiab.sendNameUpdate);
});

kiab = {
  addWidget: function (widget) {
    var widget = widget.contents().clone();
    control = $('.control', widget); 
    control[0].id = $.uuid();
    control.blur(kiab.sendUpdate);
    
    widget.appendTo($('#details .detailTable'));
    
    $('input', widget).animate({ 
      backgroundColor: '#afa'
    }, 30).animate({ 
      backgroundColor: '#fff'
    }, 3000);
  },
  sendUpdate: function () {
    $.post('update', {
      update: this.id,
      detail: this.value
    });
    this.name;
  },
  sendNameUpdate: function () {
    $.post('updateName', {
      name: this.value
    });
    this.name;
  },  
  scope: $.scope()
};
