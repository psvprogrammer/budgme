$(document).ready(function(){
    $("#table-new-in_cat").hide();
    $("#btn-cancel-new-in-cat").hide();

    $("#table-in_cat>tbody>tr>td").each(function () {

        $(this).on('click', function (event) {
            row_elem = $(this).parent();
            id = row_elem.prop('id').replace('in_cat-id_', '');

            if (event.target.tagName == 'BUTTON'){
                if (event.target.innerText == 'Save'){
                    edit_in_cat(id, row_elem);
                }
                focusout_row(id, row_elem, event);
            }
            else{
                focusin_row(id, row_elem, event);
            }
        });

        $(this).on('focusout', function (event) {
            event.preventDefault();
            active_table = $(':active').closest('table');
            if (active_table.prop('id') != 'table-in_cat'){
                event.target.focus();
            }
        });
    });
});

function focusin_row(id, row_elem, event) {
    if (!row_elem){
        row_elem = $('#in_cat-id_'+id);
    }
    row_elem.find('td').each(function () {
        $(this).prop('contenteditable', true);
    });
    $("#btn-edit-in_cat-id_"+id).show();
    $("#btn-cancel-in_cat-id_"+id).show();
    if (event){
        event.target.focus();
        event.stopPropagation();
    }

    // focusout all other rows
    $("#table-in_cat>tbody>tr").each(function () {
        current_id = $(this).prop('id').replace('in_cat-id_', '');
        if (current_id != id){
            focusout_row(current_id, $(this));
        }
    });
}

function focusout_row(id, row_elem, event) {
    if (!row_elem){
        row_elem = $('#in_cat-id_'+id);
    }
    row_elem.find('td').each(function () {
        $(this).prop('contenteditable', false);
    });
    $("#btn-edit-in_cat-id_"+id).hide();
    $("#btn-cancel-in_cat-id_"+id).hide();
    row_elem.focusout();
    if (event){
        event.stopPropagation();
    }
}

function edit_in_cat(id, row_elem) {
    test = row_elem;
    console.log('id edit: ' + id);
    // ajaxPost('/edit-in-cat', {}, function (content) {
    //     //on success
    // });
}

$("a#btn-show-new-in-cat-row").click(function(event){
    event.preventDefault();
    $(this).hide();
    $("#table-new-in_cat").show();
    $("#btn-cancel-new-in-cat").show();
});

$("#btn-cancel-new-in-cat").click(function(event){
    event.preventDefault();
    $("#table-new-in_cat").hide();
    $("#btn-cancel-new-in-cat").hide();
    $("#btn-show-new-in-cat-row").show();
});

$("a#btn-add-new-in_cat").click(function(event){
    event.preventDefault();
    //post to ajax and on success
    $("#table-new-in_cat").hide();
    $("#btn-cancel-new-in-cat").hide();
    $("#btn-show-new-in-cat-row").show();
});