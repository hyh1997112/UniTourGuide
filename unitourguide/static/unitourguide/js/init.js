(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();

  }); // end of document ready
})(jQuery); // end of jQuery name space

$(document).ready(function() {
  $('select').material_select();
  $(".dropdown-button").dropdown();
  $('.materialboxed').materialbox();
});

$('.datepicker').pickadate({
  selectMonths: true, // Creates a dropdown to control month
  selectYears: 10, // Creates a dropdown of 15 years to control year
  defaultDate: new Date(),
  format: 'yyyy-mm-dd',
});

$('.datepicker').on('mousedown',function(event){
  event.preventDefault();
})