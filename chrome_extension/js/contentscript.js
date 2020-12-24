const replaceMarker = function (str) {
  return str.replace(/<<<(.*?)>>>/g, `<span style="background-color: yellow;">$1</span>`);
};

window.onload = function () {
  if (!location.href.match(/course_[0-9]{7}?/)) {
    return;
  }
  chrome.runtime.sendMessage({ message: 'activate_icon' });
  // 検索ボックス作成
  const parent = document.getElementsByClassName('rightmostbutton')[0];
  parent.style.display = 'flex';
  parent.style.alignItems = 'center';
  const searchBoxHtml = `
    <input id="search_input" type="text" placeholder="コース内を検索" style="
      width: 20rem;
      margin-right: .5rem;
      padding: .3rem;
      padding-left: 2rem;
      border: 1px solid #999;
      border-radius: .2rem;
    ">
    <div style="
      margin-right: auto;
      color: #555;
    ">最終更新日時：<span id="last-crawling-time">不明</span></div>
    <img src="${chrome.extension.getURL('img/search_icon.png')}" style="
      position: absolute;
      width: 1rem;
    ">
  `;
  parent.insertAdjacentHTML('afterbegin', searchBoxHtml);
  $('.rightmostbutton').after(`
    <div id="search_results" style="

    "></div>
  `);
  const courseName = document.getElementById('coursename').textContent;
  $(document).on('keyup', '#search_input', function (e) {
    const searchWord = $('#search_input').val();
    if (e.keyCode !== 13 || searchWord === '') {
      return;
    }
    $('#search_results').empty();
    $.ajax({
      type: 'post',
      url: 'http://localhost:7021/search',
      data: JSON.stringify({
        course_name: courseName,
        keyword: searchWord,
      }),
      contentType: 'application/json',
      dataType: 'json',
      success: function (json_data) {
        if (json_data.results.length > 0) {
          for (const row of json_data.results) {
            $('#search_results').append(`
              <div style="
                padding: .5rem 0;
                border-top: 1px solid #ddd;
                ">
                <a href="${row.url}" target="blank" style="font-size: 1rem">${row.title}</a><br>
                …${replaceMarker(row.highlights.join('…<br>…'))}…
              </div>
            `);
          }
        } else {
          $('#search_results').append(`
              <div style="
                color: red;
              ">
                見つかりませんでした。
              </div>
            `);
        }
        let dateTime = new Date(json_data.crawling_time * 1000);
        $('#last-crawling-time').text(
          `${dateTime.toLocaleDateString()} ${dateTime.toLocaleTimeString('ja-JP')}`
        );
      },
      error: function () {
        alert('Server Error. Pleasy try again later.');
      },
    });
  });
};
