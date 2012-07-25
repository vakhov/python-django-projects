(function (window, document) {

	var styleSheet = document.createElement('style');
	styleSheet.setAttribute('media', 'screen');
	document.documentElement.firstChild.insertBefore(styleSheet, document.documentElement.firstChild.firstChild);

	var regularExpressionRunner,
	    onetimeExpressions = {},
	    regularExpressions = {};

	function getRandomProperty() {
		return '-ie-' + Math.floor(Math.random() * 10000);
	}

	function getRandomId() {
		return 'ie-' + Math.floor(Math.random() * 100000);
	}

	function addRule(selector, rule) {
		var selectors = selector.split(',');
		for (var i = 0; i < selectors.length; i++)
			styleSheet.styleSheet.addRule(selectors[i], rule);
	}

	function addOnetimeExpression(selector, expression) {
		var property = getRandomProperty();
		onetimeExpressions[property] = expression;
		addRule(selector, property + ': expression(IeStyleSheet.callOnetimeExpression("' + property + '", this), runtimeStyle.cssText += (runtimeStyle.cssText ? ";" : "") + "' + property + ': expression(\'\') !important")');
	}

	function callOnetimeExpression(property, element) {
		onetimeExpressions[property].call(element);
	}

	function addRegularExpression(selector, expression) {
		var property = getRandomProperty();
		regularExpressions[property] = { expression: expression, callbacks: {} };
		this.addRule(selector, property + ': expression(IeStyleSheet.callRegularExpression("' + property + '", this))');
	}

	function callRegularExpression(property, element) {
		if (!element.ieStyleSheetId)
			element.ieStyleSheetId = getRandomId();
		if (!regularExpressions[property].callbacks[element.ieStyleSheetId])
			regularExpressions[property].callbacks[element.ieStyleSheetId] = { element: element };
		regularExpressions[property].callbacks[element.ieStyleSheetId].active = true;
		if (regularExpressionRunner)
			return;
		regularExpressionRunner = setInterval(processRegularExpressions, 50);
	}

	function processRegularExpressions() {
		for (var property in regularExpressions) {
			var expression = regularExpressions[property];
			for (var elementId in expression.callbacks) {
				var element = expression.callbacks[elementId];
				if (!element.active) continue;
				expression.expression.call(element.element);
				element.active = false;
			}
		}
	}

	window.IeStyleSheet = {
		addRule: addRule,
		addOnetimeExpression: addOnetimeExpression,
		callOnetimeExpression: callOnetimeExpression,
		addRegularExpression: addRegularExpression,
		callRegularExpression: callRegularExpression
	};

	var unloadEvent = 'unload';

	function cleanup() {
		window.detachEvent(unloadEvent, cleanup);
		onetimeExpressions = null;
		regularExpressions = null;		
	}

	window.attachEvent(unloadEvent, cleanup);

})(window, document);