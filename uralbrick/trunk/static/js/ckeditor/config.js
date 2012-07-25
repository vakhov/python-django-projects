/*
Copyright (c) 2003-2011, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
	// Define changes to default configuration here. For example:
	config.language = 'ru';
	config.toolbar = 'Basic';
	config.toolbar_Basic = //индивидуальная настройка режима Basic
		[
		['Source', '-', 
		 'Bold', 'Italic', 'Underline', '-',
		 'JustifyLeft','JustifyCenter','JustifyRight','JustifyFull',  '-',
		 'Table', 'SpecialChar', '-',
		 'Link', 'Unlink','-',]
		];
	// config.uiColor = '#AADC6E';
};
