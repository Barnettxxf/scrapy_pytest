(function () {
    $('#commit').on('click', function (e) {
        e.preventDefault();

        let storage = $('#storage').val();
        let spider = $('#spider').val();

        superagent.get(`/filter?storage=${storage}&spider=${spider}`).end(function (err, data) {
            if (err) throw err;

            let str = '';
            for (let row of data.body.rows) {
                str = str + `<tr><td>${row.id}</td><td>${row.storage}</td><td>${row.spider}</td><td>${row.parse_func}</td><td>${row.url}</td><td>${JSON.stringify(row.meta)}</td><td><a href="/del?request_id=${row.id}">delete</a></td></td></tr>`;
            }
            console.log(str);
            $('#content').html(str);
            $('.pagination').html('');
        });
    })
})();
