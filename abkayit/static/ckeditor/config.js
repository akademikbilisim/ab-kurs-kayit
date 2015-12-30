/*
Copyright (c) 2003-2010, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{

    config.toolbar = [
        ['Source', '-',
         'Preview', '-',
         'Cut', 'Copy', 'Paste', '-',
         'Undo', 'Redo', '-',
         'FontSize', '-',
         'Link','Unlink', '-', '/',
         'Bold', 'Italic', 'Underline', '-',
         'NumberedList', 'BulletedList', '-',
        'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'
        ]
    ],
    config.toolbarCanCollapse = false,
    config.resize_enabled = false,
    config.removePlugins = 'elementspath',
    config.pasteFromWordRemoveStyles = false,
    config.pasteFromWordRemoveFontStyles = false,


    config.width = 800,
    config.skin = 'office2003'

	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
};
