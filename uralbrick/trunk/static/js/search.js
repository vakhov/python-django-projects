$(document).ready(function() {
	
	var current_path = window.location.pathname;
	if (current_path == '/production/') {
		var url = '/api/search/alphabet/';
	};
	if (current_path.split('/')[1] == 'qa') {
		var url = '/api/search/alphabet_tag/';
	};

	function selected(){
		$('.alphabet_filter').find('a.colored_bgColor').each(function(){
			if($(this).hasClass('selected')){
				$(this).removeClass('selected');
			}
		});
	}
	
	var alphabet = '';
	$('.alphabet_filter').find('a.colored_bgColor').each(function(){
		$(this).unbind('click');
		$(this).click(function() {
			selected();
			if(alphabet != $(this).text()){
				alphabet = $(this).text();
				self = $(this);
				$('.alphabet_result_container').slideUp(function() {
					$.ajax({
						async: true,
						type: 'POST',
						url: url,
						data: {
							'alphabet': $.toJSON(alphabet),
						},
						success: function(data) {
							var data = JSON.parse(data);
							var html = '<div class="alphabet_result_letter colored_bgColor">' + alphabet + '</div>';
							var alpha_str = '<span class="colored_bgColor">' + alphabet + '</span>';
							var alpha_str_lower = '<span class="colored_bgColor">' + alphabet.toLowerCase() + '</span>';
							$.each(data, function() {
								if (!this.caption) {
									html += '<span class="alphabet_result_item">&nbsp;</span>';
								}
								else {
								//$.each(this, function() {
									if (current_path.split('/')[1] == 'qa') {
										tag_path = '/qa/tag/';
									}
									else {
										tag_path = '';
									};
									var istr = '<span class="alphabet_result_item"><a href="' + tag_path + this.path + '/" class="whiteLink">' + this.caption + '</a></span>';
									html += istr.replace('||', alpha_str_lower).replace('|', alpha_str);
								//});
								}
							});
							self.addClass('selected');
							$('.alphabet_result_letter').text(alphabet);
							$('.alphabet_result').html(html);
							$('.alphabet_result_container').slideDown();
						}
					});
				});
			}else{
				$('.alphabet_result_container').slideUp();
				alphabet = '';
			}
			return false;
		});
	});
});