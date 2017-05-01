//= require jquery
//= require bootstrap

$(document).ready(function() {
  var $nav = $('#nav');

  $('.col-md-9 section').each(function() {
    var title = $(this).find('h2').text();
    var id = $(this).attr('id');
    $li = $('<li><a href="#'+id+'">'+title+'</a></li>');

    var $sub = $('<ul class="nav"></ul>');
    $(this).find('section').each(function() {
      var subtitle = $(this).find('h4').text();
      var subid = $(this).attr('id');
      $sub.append($('<li><a href="#'+subid+'">'+subtitle+'</a></li>'));
    });

    if ($sub.find('li').length)
      $sub.appendTo($li);

    $li.appendTo($nav);
  });

  $('#nav > li > a').each(function() {
    if (!$(this).text())
      $(this).remove();
  });

  $('body').scrollspy('refresh');

  $('p img').each(function() {
    if (!$(this).siblings().length)
      $(this).parent().css('text-align', 'center');
  });
});

$('#nav').affix({
  offset: 150
})
