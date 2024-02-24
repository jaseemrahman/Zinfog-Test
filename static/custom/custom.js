function show_edit_modal(id){
    $("#hid").val(id);

    $("#modaldemo5").modal('show');
  }



function changefilterstatus(id,vl) {
  
    page=$("#page").val();


  var search = $('#searchkey').val()
  var status = $('#status').val()
  var url = $('#url').val()
  $.ajax({
    url: url,
    type: 'GET',
    data: {searchkey:search,page:page,status:status,id:id,vl:vl,type:1},

    success: function(data) {

      $("#data_table").html(data.template)


    }
});
}


function filterstudent(data) {
    var page = '1'
      if(data != 'None'){
        page=data
      }
  
      var search = $('#searchkey').val()
      var status = $('#status').val()
      var url = $('#url').val()
      $.ajax({
        url: url,
        type: 'GET',
        data: {searchkey:search,page:page,status:status},
  
        success: function(data) {
  
          $("#data_table").html(data.template)
  
  
        }
    });
    }

    function updatestudent(id) {
        page=$("#page").val();
          var mark = $('#mark'+id).val()
          var url = $('#url').val()
          $.ajax({
            url: url,
            type: 'GET',
            data: {mark:mark,page:page,id:id},
      
            success: function(data) {
      
              $("#data_table").html(data.template)
      
      
            }
        });
        }
    