$(document).ready(function(){
    $("#table-new-in_cat").hide();
    $("#btn-cancel-new-in-cat").hide();

    $("#table-in_cat>tbody>tr>td").each(function () {

        $(this).on('click', function (event) {
            row_elem = $(this).parent();
            id = row_elem.prop('id').replace('in_cat-id_', '');

            if (event.target.tagName == 'BUTTON'){
                if (event.target.innerText == 'Save'){
                    save_in_cat(id);
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

    // row_elem.find('td.field').each(function () {
    //     $(this).prop('contenteditable', true);
    // });
    row_elem.find('td.field').each(function () {
        p = $(this).find('p');
        input = $(this).find('input');

        // input.prop('value', p.html());
        p.hide();
        input.show();
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

    // row_elem.find('td.field').each(function () {
    //     $(this).prop('contenteditable', false);
    // });
    row_elem.find('td.field').each(function () {
        p = $(this).find('p');
        input = $(this).find('input');

        // p.html(input.prop('value'));
        p.show();
        input.hide();
    });

    $("#btn-edit-in_cat-id_"+id).hide();
    $("#btn-cancel-in_cat-id_"+id).hide();
    row_elem.focusout();
    if (event){
        event.stopPropagation();
    }
}

function save_in_cat(id) {
    name_elem = $('input#name-id_' + id);
    descr_elem = $('input#description-id_' + id);
    data = {
        id: id,
        name: name_elem.prop('value'),
        description: descr_elem.prop('value'),
    };
    ajaxPost('/edit-in-cat', data, function (content) {
        //on success
        console.log('ajaxPost success!');
        name_elem.parent().find('p').html(name_elem.prop('value'));
        descr_elem.parent().find('p').html(descr_elem.prop('value'));
    });
}

$("a#btn-show-new-in-cat-row").click(function(event){
    event.preventDefault();
    $(this).hide();
    $("#table-new-in_cat").show();
    // $("#btn-cancel-new-in-cat").show();
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