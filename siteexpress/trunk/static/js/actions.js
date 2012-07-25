// Menu

$(document).ready(function(){

	// Tables
	$("#text table:not(.not-decorated), #position table:not(.not-decorated)").each(function() {
		if ($(this).find("th").length==0) {
			$(this).find("tr:nth-child(odd)").addClass("odd");
			$(this).find("tr:nth-child(even)").addClass("even");
			$(this).find("td").css("border-width","1px 1px 0 0").css("border-style","solid");
			$(this).find("tr td:first-child").css("border-width","1px 1px 0 1px");
			$(this).find("tr:last-child td").css("border-width","1px 1px 1px 0");
			$(this).find("tr:last-child td:first-child").css("border-width","1px");
		}
		else {
			$(this).find("tr:nth-child(odd)").addClass("even");
			$(this).find("tr:nth-child(even)").addClass("odd");
			$(this).find("td").css("border-width","0 1px 1px 0").css("border-style","solid");
			$(this).find("tr td:first-child").css("border-width","0 1px 1px 1px");
			$(this).find("th").css("border-width","1px 1px 1px 0").css("border-style","solid");
			$(this).find("th:first").css("border-width","1px");
		}
	});
	$("#catalog table td").css("border-style","dashed");
	$("#catalog table th").css("border-bottom","0");
	$("#catalog table th:last-child").css("border-width","0");
	
	// Template2 news/specials h2
	// if ($("#template2").length!=0 || $("#template5").length!=0) {
	// 	if ($("#news").length==0 && $("#specials").length==0) {
	// 		$(".collapse").hide();
	// 	}
	// 	else if ($("#news").length==0) {
	// 		$(".right .collapse:first").hide();
	// 		$(".right .collapse:last").removeClass("span-8").addClass("span-16");
	// 		$("#specials li").css("width","50%").css("float","left");
	// 	// }
	// 	// else if ($("#specials").length==0) {
	// 	// 	$(".right .collapse:last").hide();
	// 	// 	$(".right .collapse:first").removeClass("span-8").addClass("span-16");
	// 	// }
	// }
	// Temp
});
