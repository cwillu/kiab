$(function () {
  $('.palette .widget').click(function () {
    var widget = $('.widgetPrototype .detailTable', this);
    kiab.addWidget(widget);
  });
  $('.control', $('#details')).blur(kiab.sendUpdate);
  $('.name', $('#details')).blur(kiab.sendNameUpdate);
  $('textarea', $('#comments')).blur(kiab.sendComment);
});

kiab = {
  session_uuid: $.uuid(),
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
    $.post('updateDetail', {
      update: this.id,
      detail: this.value
    });
  },
  sendNameUpdate: function () {
    $.ajax({
      type: "POST",
      url: 'updateName',
      data: {
        name: this.value,
        uuid: $("#details input[name='uuid']")[0].value
      },
      complete: function (http) {
        if (http.status === 201) {
          top.location.href = http.getResponseHeader('Location');
        }        
      }      
    });
  },  
  sendComment: function () {
     $.ajax({
      type: "POST",
      url: 'addComment',
      data: {
        session_uuid: kiab.session_uuid,
        uuid: this.id,
        comment: this.value
      },
      complete: function (http) {
        if (http.status === 205) {
          window.location.reload(false);
        }        
      }      
    });
  },
  scope: $.scope()
};






















