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
  util: {
    commonResponses: function (http) {
      if (http.status / 100 >> 0 === 2) {
        html = http.responseText;
        if (html) {
          $(html).insertBefore($('#comments .header:last'));
        }
      }

      if (http.status === 201) {
        if (http.getResponseHeader('x-location')) {
          top.location.href = http.getResponseHeader('x-location');
        }        
      }        
    }
  },
  contact: {  
    instance_uuid: $.uuid(),
    addWidget: function (widget) {
      var widget = widget.contents().clone();
      control = $('.control', widget); 
      control[0].id = $.uuid();
      control.blur(kiab.contact.sendUpdate);
      
      widget.appendTo($('#details .detailTable'));
      
      $('input', widget).focus().animate({ 
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
          instance_uuid: kiab.instance_uuid,
          update: this.id,
          detail: this.value,
          uuid: $("#details input[name='uuid']")[0].value
        },
        complete: kiab.util.commonResponses,        
      });
    },
    sendNameUpdate: function () {
      $.ajax({
        type: "POST",
        url: 'updateName',
        data: {
          instance_uuid: kiab.instance_uuid,        
          name: this.value,
          uuid: $("#details input[name='uuid']")[0].value
        },
        complete: kiab.util.commonResponses,        
      });
    },  
    sendComment: function () {
      var textarea = this;
      $.ajax({
        type: "POST",
        url: 'addComment',
        data: {
          instance_uuid: kiab.instance_uuid,
          uuid: this.id,
          comment: this.value,
          uuid: $("#details input[name='uuid']")[0].value
        },
        complete: function (http) {
          kiab.util.commonResponses(http);
          if (http.status / 100 >> 0 === 2) {
            textarea.value = '';
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
        this.value = '';
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






















