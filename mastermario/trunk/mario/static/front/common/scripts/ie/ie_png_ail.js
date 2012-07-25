(function (IeStyleSheet, addOnetimeExpression, addRule) {

	function IePngAil(element, sizing) {
		var src;
		if (element.tagName == 'IMG') {
			src = element.src;
			element.width = element.width;
			element.height = element.height;
			sizing = sizing || 'scale';
			element.src = 'path/to/transparent/pixel.gif';
			/** todo replace with: http://www.cssplay.co.uk/ie/ie6-pngfix.html */
		}
		else {
			src = element.currentStyle.backgroundImage.match(/url\("(.+?)"\)/i);
			if (src) {
				src = src[1];
				sizing = sizing || 'crop';
				element.runtimeStyle.backgroundImage = 'none';
			}
		}
		if (src)
			element.runtimeStyle.filter = 'progid:DXImageTransform.Microsoft.AlphaImageLoader(src="' + src + '", sizingMethod="' + sizing + '")';
	};

	addOnetimeExpression.call(IeStyleSheet, '.ie-png-ail', function () { IePngAil(this); });
	addRule.call(IeStyleSheet, '.ie-png-ail a', 'position: relative');

	addOnetimeExpression.call(IeStyleSheet, '.ie-png-ail-scale', function () { IePngAil(this, "scale"); });
	addRule.call(IeStyleSheet, '.ie-png-ail-scale a', 'position: relative');

	addOnetimeExpression.call(IeStyleSheet, '.ie-png-ail-crop', function () { IePngAil(this, "crop"); });
	addRule.call(IeStyleSheet, '.ie-png-ail-crop a', 'position: relative');

	addOnetimeExpression.call(IeStyleSheet, '.ie-png-ail-image', function () { IePngAil(this, "image"); });
	addRule.call(IeStyleSheet, '.ie-png-ail-image', 'zoom: 1');
	addRule.call(IeStyleSheet, '.ie-png-ail-image a', 'position: relative');

})(IeStyleSheet, IeStyleSheet.addOnetimeExpression, IeStyleSheet.addRule);
