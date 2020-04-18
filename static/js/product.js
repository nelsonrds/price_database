$(document).ready(function () {
  $(".btndelete").click(function (e) {
    $.ajax({
      url: "/product/" + e.currentTarget.id,
      type: "DELETE",
      context: document.body
    }).done(function (data) {
      resp = jQuery.parseJSON(data);
      $("#" + resp.product).remove();
    });
  });
});