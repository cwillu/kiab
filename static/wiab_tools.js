/*jslint browser: true */
/*jslint eqeqeq: true */
/*jslint forin: true */
/*jslint bitwise: true */
/*jslint plusplus: true */
/*jslint white: true */
/*predef $,jQuery */

jQuery.uuid = function () {
  var chunk = function () {
  	return ((Math.random()+1)*0x10000 | 0).toString(16).substring(1)
  }

  return chunk() + chunk() + "-" + chunk() + "-"chunk() + "-" + chunk() + "-" + chunk() + chunk() + chunk()
};

jQuery.scope = function () {      
  var intervals = [];
  var timeouts = [];
  var cancels = [];
  var scope = {      
    stop: function () {
      while (timeouts.length > 0) {
        clearTimeout(timeouts.pop());
      }
      while (intervals.length > 0) {
        clearInterval(intervals.pop());
      }
      while (cancels.length > 0) {
        cancels.pop().call(this);
      }
    },
    after: function (func) {
      cancels.push(func);
      return scope;
    },
    bind: function (query, bindings) {
      cancels.push(function () {
        for (var event in bindings) {
          query.unbind(event, bindings[event]);
        }
      });
      
      for (var event in bindings) {          
        query.bind(event, bindings[event]);
      }        
      return scope;
    },
    interval: function (func, time) {
      intervals.push(setInterval(func, time));
      return scope;
    },
    timeout: function (func, time) {
      timeouts.push(setTimeout(func, time));
      return scope;
    }
  };
  return scope;
};
jQuery.False = function () {
  return false;
};
jQuery.fn.whichParent = function (node) {
  var query = this;
  var target = [];
  $.each(node.parents().andSelf().get(), function () {
    var parent = this;
    target = query.filter(function () { 
      return this === parent; 
    });
    if (target.length > 0) {
      return false;
    }
  });
  return target;
};
jQuery.error = function (msg) {
  console.log.apply(console.log, arguments);
  alert('Error');
};
jQuery.mirror = function (orientation) {  
  var horizontal = (
    orientation === false ||
    orientation === 'west' || 
    orientation === 'east' || 
    orientation === 'horizontal' ||
    orientation === 'x' ||
    orientation === 'left' ||
    orientation === 'width');
  var vertical = !horizontal;
    
  var d = {
    left: horizontal ? 'left' : 'top',
    width: horizontal ? 'width' : 'height',
    west: horizontal ? 'west' : 'north',
    east: horizontal ? 'east' : 'south',
    horizontal: horizontal ? 'horizontal' : 'vertical',
    x: horizontal ? 'x' : 'y'
  };
  $.extend(d, {
    top: vertical ? 'left' : 'top',
    height: vertical ? 'width' : 'height',
    north: vertical ? 'west' : 'north',
    south: vertical ? 'east' : 'south',
    vertical: vertical ? 'horizontal' : 'vertical',
    y: vertical ? 'x' : 'y'
  });
  return d;
};



