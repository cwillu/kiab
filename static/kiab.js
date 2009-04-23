$(function () {
  $('.palette .widget').click(function () {
    var widget = $('.widgetPrototype .detailTable', this);
    kiab.contact.addWidget(widget);
  });
  $('.control', $('#details')).blur(kiab.contact.sendUpdate);
  $('.name', $('#details')).blur(kiab.contact.sendNameUpdate);
  $('textarea', $('#comments')).blur(kiab.contact.sendComment);

  $("input[name='search']").focus(kiab.search.prepareField);
  $("input[name='search']").blur(kiab.search.cleanUpField);
});

kiab = {
 contact: {
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
      $.ajax({
        type: "POST",
        url: "updateDetail",
        data: {
          update: this.id,
          detail: this.value,
          uuid: $("#details input[name='uuid']")[0].value
        },
        complete: function (http) {
          if (http.status === 201) {
            top.location.href = http.getResponseHeader('Location');
          }        
        }
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
          comment: this.value,
          uuid: $("#details input[name='uuid']")[0].value
        },
        complete: function (http) {
          if (http.status === 205) {
            window.location.reload(false);
          } else if (http.status === 201) {
            top.location.href = http.getResponseHeader('Location');
          }        
        }      
      });
    }
  },
  search: {
    prepareField: function () {
      if (!('initialValue' in kiab.search)) {
        kiab.search.initialValue = this.value;
      }
      if (this.value === kiab.search.initialValue) {
        this.value = ''
      } else {
        $(this).select();
      }
    },
    cleanUpField: function () {
      if (!('initialValue' in kiab.search)) {
        return alert('initialValue for search field was never set?  Weird.');
      }
      if ($.trim(this.value) === '') {
        this.value = kiab.search.initialValue;
      }

    }
  },
  scope: $.scope()
};






















