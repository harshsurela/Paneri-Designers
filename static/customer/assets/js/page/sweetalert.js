"use strict";


$("#swal-14").click(function () {
  swal('', 'Response has been Sent Successfully', 'success');
});
$("#swal-3").click(function () {
  swal('', 'Product Details Updated Successfully', 'success');
});
$("#swal-4").click(function () {
  swal('', 'Customised Order Has been Added Successfully', 'success');
});
$("#swal-6,#swal-7,#swal-8,#swal-10,#swal-11,#swal-13,#swal-16,#swal-17,#swal-18,#swal-19,#swal-20,#swal-21,#swal-22,#swal-24,#swal-25,#swal-26").click(function () {
  swal({
    title: 'Are you sure?',
    text: 'Once deleted, you will not be able to recover this record!',
    icon: 'warning',
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {
        window.location.href="{% url 'delrecord' p.id  %}";
        swal('Poof! Record has been deleted!', {
          icon: 'success',
        });
      } else {
        swal('Your Record is safe!');
      }
    });
});
$("#swal-12").click(function () {
  swal('', 'Report has been Generated Successfully', 'success');
});
$("#swal-23").click(function () {
  swal('', 'Product has been Added Successfully', 'success');
});