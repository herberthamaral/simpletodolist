$.tastypie_ajax = function(url, type, data, success){
    $.ajax({
      type: type,
      url: url,
      data: typeof(data)=="object"?JSON.stringify(data):data,
      success: success,
      complete:function(jqXHR, status){ console.log(status)},
      dataType: "json",
      contentType: "application/json"
    });
}

var todos = [];
var user = null;
var current_id = 0;
var ws = null;


$('#page-1').live('pageinit',function(){
    get_user(get_tasks);
    $('#txttask').keydown(add_task_event);
    $('a[ref=todo]').live('click',edit_todo_event);
    $('#submit-changes').click(function(){
        var id = $(this).attr('rel');        
        var todo = get_todo_by_id(id);
        todo.name = $('#name').val();
        todo.done = $('#done').is(':checked');
        $.tastypie_ajax('/api/v1/todo/'+id+'/', 'PUT', JSON.stringify(todo), function(){
            get_tasks();
            alert('Alterado com sucesso');
            window.history.back();
            ws.send('refresh');
        });
    });

    $('#exclude-task').click(function(){
        var id = $(this).attr('rel');
        if (confirm('Tem certeza?'))
        {
            $.tastypie_ajax('/api/v1/todo/'+id+'/','DELETE', '', function(){
                alert('excluido com sucesso!');
                ws.send('refresh');
                get_tasks();
                window.history.back();
            });
        }
    });

    $('#refresh').click(function(){
        get_tasks();
    });

    //$('#remove-done').click(function(){
    //    if(confirm('tem certeza?')){
    //        var url = '/api/v1/todo/?done=1';
    //        $.tastypie_ajax(url, 'DELETE', '', function(){
    //            get_tasks();
    //        });
    //    }
    //});
});


get_user = function(callback){
    $.tastypie_ajax('/api/v1/user/', 'GET', '', function(data){
        user = data.objects[0];
        init_websocket();
        if (typeof(callback) == "function")
            callback();
    });
}

init_websocket = function(){
    if ("WebSocket" in window)
        ws = new window.WebSocket('ws://localhost:8888/');
    else
        ws = new window.MozWebSocket('ws://localhost:8888/');
    ws.onopen = function(){
        ws.send('user:'+user.username);
    }
    ws.onmessage = function(e){
        if (e.data == 'refresh')
            get_tasks();
    }
}

get_tasks = function(){
    $.tastypie_ajax('/api/v1/todo/','GET','',function(data){
        var items = data.objects;
        todos = data.objects;
        var template = $('#item-template').html()
        $('#todo').html('');
        for(i=0;i<items.length;i++){
            var item = $.tmpl(template,items[i]);
            if (items[i].done)
                item = $(item).css('text-decoration','line-through');
            $('#todo').append(item).listview('refresh');
        }
    });
}

add_task_event = function(evt){
    if (evt.keyCode == 13){
        add_task($(this).val());
        $(this).blur();
    }
}
add_task = function(task){
   var data = {name: task, user: user.resource_uri};
   $.tastypie_ajax('/api/v1/todo/', 'POST', JSON.stringify(data), get_tasks);
   ws.send('refresh');
}

edit_todo_event = function(){
    window.location.href = "#page-2";
    var id = $(this).attr('rel');
    var todo = get_todo_by_id(id);
    $('#id').val(id);
    $('#name').val(todo.name);
    try{
        $('#done').attr('checked', todo.done).checkboxradio('refresh');
    }catch(e){}
    $('#submit-changes').attr('rel', todo.id);
    $('#exclude-task').attr('rel', todo.id);
}

get_todo_by_id = function(id){
    for (i=0;i<todos.length;i++){
        if (todos[i].id == id){
            return todos[i];
        }
    }
}
