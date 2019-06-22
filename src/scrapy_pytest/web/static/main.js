(function () {
    $('select').on('change', function (e) {
        // e.preventDefault();

        let storage = $('#storage').val().trim();
        let spider = $('#spider').val().trim();

        superagent.get(`/filter?storage=${storage}&spider=${spider}`).end(function (err, data) {
            if (err) throw err;

            let str = '';
            for (let row of data.body.rows) {
                str = str + `<tr><td><input type="checkbox"></td><td>${row.id}</td><td>${row.storage}</td><td>${row.spider}</td><td>${row.parse_func}</td><td>${row.url}</td><td>${JSON.stringify(row.meta)}</td><td class="for-delete"><a href="#">delete</a></td></td></tr>`;
            }
            console.log(str);
            $('#content').html(str);
            $('.pagination').html('');
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
            let req_id = $(this).parent().parent().attr('data-id');
            if (req_id) {
                superagent.get(`/del?request_id=${req_id}`).end(function (err, data) {
                    if (err) throw err;
                    if (data.body.success) {
                        req_id.remove();
                    }
                });
            }
        })
    })
})();

(function () {
    $('.for-delete').on('click', function (e) {
        e.preventDefault();

        let req_id = $(this).parent().parent().attr('data-id');
        if (req_id) {
            superagent.get(`/del?request_id=${req_id}`).end(function (err, data) {
                if (err) throw err;
                if (data.body.success) {
                    req_id.remove();
                }
            });
        }
    })
})();