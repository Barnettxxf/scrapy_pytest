(function () {
    $('select').on('change', function (e) {
        // e.preventDefault();

        let storage = $('#storage').val().trim();
        let spider = $('#spider').val().trim();

        superagent.get(`/filter?storage=${storage}&spider=${spider}`).end(function (err, data) {
            if (err) throw err;

            let str = '';
            for (let row of data.body.rows) {
                str = str + `<tr><td><input type="checkbox"></td><td>${row.id}</td><td>${row.storage}</td><td>${row.spider}</td><td>${row.parse_func}</td><td>${row.url}</td><td>${JSON.stringify(row.meta)}</td></tr>`;
            }
            let page_str = '<li class="previous disabled unavailable"><a> &laquo; </a></li><li class="active"><a>1</a></li>';
            let dot_page = false;
            for (let i = 2; i < data.body.total / data.body.per_page + 1; i++) {
                if (i > 5 || i < (data.body.total / data.body.per_page + 1) - 5) {
                    if (!dot_page) {
                        page_str += `<li class="disabled unavailable"><a>...</a></li>`;
                        dot_page = true;
                    }
                } else {
                    page_str += `<li><a href="/?page=${i}&$per_page=${data.body.per_page}&storage=${storage}&spider=${spider}">${i}</a></li>`;
                }
            }
            if (data.body.total / data.body.per_page > 1) {
                page_str += `<li class="next"><a href="/?page=2&per_page=${data.body.per_page}&storage=${storage}&spider=${spider}">&raquo;</a></li>`;
            } else {
                page_str += `<li class="next disabled unavailable"><a href="#">&raquo;</a></li>`;
            }
            $('#content').html(str);
            $('.pagination').html(page_str);
        });
    })
})();


(function () {
    $('#select-all').on('click', function (e) {
        let is_select_all = $('#select-all').prop('checked');
        if (is_select_all) {
            $('input[type=checkbox]').each(function (index, item) {
                $(this).attr('checked', true);
            })
        } else {
            $('input[type=checkbox]').each(function (index, item) {
                $(this).attr('checked', false);
            })
        }
    });
})();

(function () {
    $('#delete').on('click', function (e) {
        e.preventDefault();
        $('input:checkbox:checked').each(function (index, item) {
            let tr = $(this).parent().parent();
            let req_id = tr.attr('data-id');
            if (req_id) {
                superagent.get(`/del?request_id=${req_id}`).end(function (err, data) {
                    if (err) throw err;
                    if (data.body.success) {
                        tr.remove();
                    }
                });
            }
        })
    })
})();