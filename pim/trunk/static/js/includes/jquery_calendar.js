(function($) {

    function calendarWidget(el, params) {

        var now = new Date();
        var thismonth = now.getMonth();
        if ($('.ie').length == 0) var thisyear = now.getYear() + 1900; else var thisyear = now.getYear();
        var thisdate = now.getDate();

        var opts = {
            month: thismonth,
            year: thisyear
        };

        $.extend(opts, params);

        var monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
        var dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
        month = i = parseInt(opts.month - 1);
        year = parseInt(opts.year);
        var m = 0;
        var table = '';

        // next month
        if (month == 11) {
            var next_month = '<a href="?month=' + 1 + '&amp;year=' + (year + 1) + '" title="' + monthNames[0] + ' ' + (year + 1) + '">' + monthNames[0] + ' ' + (year + 1) + '</a>';
        } else {
            var next_month = '<a href="?month=' + (month + 2) + '&amp;year=' + (year) + '" title="' + monthNames[month + 1] + ' ' + (year) + '">' + monthNames[month + 1] + ' ' + (year) + '</a>';
        }

        // previous month
        if (month == 0) {
            var prev_month = '<a href="?month=' + 12 + '&amp;year=' + (year - 1) + '" title="' + monthNames[11] + ' ' + (year - 1) + '">' + monthNames[11] + ' ' + (year - 1) + '</a>';
        } else {
            var prev_month = '<a href="?month=' + (month) + '&amp;year=' + (year) + '" title="' + monthNames[month - 1] + ' ' + (year) + '">' + monthNames[month - 1] + ' ' + (year) + '</a>';
        }

        //$("#c_month").text(monthNames[month]);
        //$("#c_year").text(year);
        // uncomment the following lines if you'd like to display calendar month based on 'month' and 'view' paramaters from the URL
        //table += ('<div class="nav-prev">'+ prev_month +'</div>');
        //table += ('<div class="nav-next">'+ next_month +'</div>');
        table += ('<table class="calendar-month " ' + 'id="calendar-month' + i + ' " cellspacing="0" cellpadding="0">');

        table += '<tr>';

        for (d = 0; d < 7; d++) {
            table += '<th class="weekday"><ins>' + dayNames[d] + '</ins></th>';
        }

        table += '</tr>';

        var days = getDaysInMonth(month, year);
        var firstDayDate = new Date(year, month, 1);
        var firstDay = firstDayDate.getDay();

        var prev_days = getDaysInMonth(month, year);
        var firstDayDate = new Date(year, month, 1);
        var firstDay = firstDayDate.getDay();

        var prev_m = month == 0 ? 11 : month - 1;
        var prev_y = prev_m == 11 ? year - 1 : year;
        var prev_days = getDaysInMonth(prev_m, prev_y);
        firstDay = (firstDay == 0 && firstDayDate) ? 6 : firstDay - 1;

        var i = 0;
        var cur_class;
        for (j = 0; j < 42; j++) {
            if (thisdate == (j - firstDay + 1) && (thismonth + 1) == opts.month && (thisyear) == opts.year) cur_class = ' cur'; else cur_class = '';
            if ((j < firstDay)) {
                table += ('<td class="other-month"><ins><span class="day">' + (prev_days - firstDay + j + 1) + '</span></ins></td>');
            } else if ((j >= firstDay + getDaysInMonth(month, year))) {
                i = i + 1;
                table += ('<td class="other-month"><ins><span class="day">' + i + '</span></ins></td>');
            } else {
                var linkObj = $('#calendar .links .' + (j - firstDay + 1) + '_' + opts.month + '_' + opts.year);
                if (linkObj.length != 0)
                    table += ('<td class="current-month link day' + (j - firstDay + 1) + cur_class + '"><ins><a href="' + linkObj.text() + '"><span class="day">' + (j - firstDay + 1) + '</span></a></ins></td>');
                else
                    table += ('<td class="current-month day' + (j - firstDay + 1) + cur_class + '"><ins><span class="day">' + (j - firstDay + 1) + '</span></ins></td>');
            }
            if (j % 7 == 6)  table += ('</tr>');
        }

        table += ('</table>');

        el.html(table);
    }

    function getDaysInMonth(month, year) {
        var daysInMonth = [31,28,31,30,31,30,31,31,30,31,30,31];
        if ((month == 1) && (year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))) {
            return 29;
        } else {
            return daysInMonth[month];
        }
    }


    // jQuery plugin initialisation
    $.fn.calendarWidget = function(params) {
        calendarWidget(this, params);
        return this;
    };


})(jQuery);
