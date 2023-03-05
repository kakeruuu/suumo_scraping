function getData(url) {
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error(error);
        });
}

function createRegions() {
    getData("http://localhost:8000/read_region")
        .then(data => {
            const selectBox = document.getElementById("region_select_box");
            selectBox.innerHTML = `
                        <option value="">選択してください</option>
                        ${data.map(region => `<option value="${region.region_id}">${region.region}</option>`).join("")}
                    `;
        })
        .catch(error => {
            console.error(error);
        })
}


function createPrefecturesSelectBox() {
    const regionSelectBox = document.getElementById("region_select_box");
    const prefecturesSelectBox = document.getElementById("prefecture_select_box");
    const regionId = regionSelectBox.value;

    if (!regionId) {
        prefecturesSelectBox.innerHTML = "";
        return;
    }

    getData(`http://localhost:8000/read_prefecture?region_id=${regionId}`)
        .then(data => {
            prefecturesSelectBox.innerHTML = `
                        <option value="">選択してください</option>
                        ${data.map(prefecture => `<option value="${prefecture.prefecture_id}">${prefecture.prefecture}</option>`).join("")}
                    `;
        })
        .catch(error => {
            console.error(error);
        })
}


async function createCityCheckBoxes() {
    const prefecturesSelectBox = document.getElementById("prefecture_select_box");
    const prefectureId = prefecturesSelectBox.value
    const cityGroupUrl = `http://localhost:8000/read_city_group?prefecture_id=${prefectureId}`;
    const cityGroupRes = await fetch(cityGroupUrl);
    const cityGroupJson = await cityGroupRes.json();

    const trs = await Promise.all(cityGroupJson.map(async (group) => {
        const cityUrl = `http://localhost:8000/read_city?group_id=${group.group_id}`;
        const cityRes = await fetch(cityUrl);
        const cityJson = await cityRes.json();

        const cities = cityJson.map(city => `
        <label>
          <input type="checkbox" name="${city.city}" value="${city.city_id}">
          ${city.city}
        </label>
      `).join('');

        const citiesTd = `<td>${cities}</td>`;
        const groupTh = `<th><label><input type="checkbox" name="${group.city_group}" value="${group.group_id}">${group.city_group}</label></th>`;
        return `<tr>${groupTh}${citiesTd}</tr>`;
    }));

    const table = document.createElement('table');
    const tbody = document.createElement('tbody');
    tbody.innerHTML = trs.join('');
    table.appendChild(tbody);

    const cityCheckBoxes = document.getElementById("city_checkboxes")
    const existingTable = cityCheckBoxes.querySelector("table");
    if (existingTable) {
        existingTable.remove();
    }
    cityCheckBoxes.appendChild(table);

    const ths = table.querySelectorAll("th");
    for (const th of ths) {
        th.addEventListener("click", () => {
            const isChecked = th.querySelector("input").checked;
            const inputs = th.parentElement.querySelectorAll("td input");
            for (const input of inputs) {
                if (input) {
                    input.checked = isChecked;
                }
            }
        });
    }
}





// TODO:thは完璧なので見た目とtdをリスト形式にする
// TODO:グループの項目をクリックしたら、そのグループ内の市区町村全てをチェックできるようにする
window.onload = function () {
    createRegions()
}