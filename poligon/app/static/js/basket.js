function basket_edit_add(position_id, size_id) 
{
	$.get("/api/basket/add/" + position_id + "/" + size_id + "/?rnd="+Math.random(), function(d) { window.location.reload() });
}

function basket_edit_del(position_id, size_id)
{
	$.get("/api/basket/delete/" + position_id + "/" + size_id + "/?rnd="+Math.random(), function(d) { window.location.reload() });
}

function change_size(position_id, old_size_id, new_size_id)
{
	$.get("/api/basket/change_size/" + position_id + "/" + old_size_id + "/" + new_size_id + "/?rnd="+Math.random(), function(d) { window.location.reload() });
}
