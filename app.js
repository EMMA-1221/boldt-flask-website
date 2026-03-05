// element grabber
function r_e(id) {
  return document.querySelector(`#${id}`);
}

// hide
function hide() {
  r_e("home_div").classList.add("is-hidden");
  r_e("guidance_div").classList.add("is-hidden");
  r_e("estimator_div").classList.add("is-hidden");
  //   r_e("guidance_dropdown").classList.remove("is-active");
}

// home button
r_e("home_button").addEventListener("click", () => {
  hide();
  r_e("home_div").classList.remove("is-hidden");
});

// guidance button
r_e("guidance_button").addEventListener("click", () => {
  hide();
  r_e("guidance_div").classList.remove("is-hidden");
});

// estimator button
r_e("estimator_button").addEventListener("click", () => {
  hide();
  r_e("estimator_div").classList.remove("is-hidden");
});

// guidance dropdown button
r_e("guidance_filter").addEventListener("change", () => {
  // NEEDS TO BE CODED
});

// tool button
r_e("tool_button").addEventListener("click", () => {
  r_e("tool_hints").classList.add("is-hidden");
  r_e("estimator_tool").classList.remove("is-hidden");
  r_e("tool_button").classList.add("is-active");
  r_e("hints_button").classList.remove("is-active");
});

// hints button
r_e("hints_button").addEventListener("click", () => {
  r_e("estimator_tool").classList.add("is-hidden");
  r_e("tool_hints").classList.remove("is-hidden");
  r_e("tool_button").classList.remove("is-active");
  r_e("hints_button").classList.add("is-active");
});

// clear form
r_e("clear_form").addEventListener("click", () => {
  r_e("Industry").value = "empty";
  r_e("Revenue").value = "";
  r_e("Length").value = "";
  r_e("Contract").value = "empty";
  r_e("Zip").value = "";
  for (let x = 1; x <= 10; x++) {
    r_e(`team_mem_${x}`).value = "";
    r_e(`team_mem_${x}_role`).value = "";
  }
  let tbl_val = [
    "overall_val",
    "industry_val",
    "revenue_val",
    "length_val",
    "contract_val",
    "average_val",
    "result_val",
  ];
  tbl_val.forEach((cell) => {
    r_e(`${cell}`).innerHTML = "";
  });
  r_e("errors_list").innerHTML = "";
});

let team_names = ["member1", "member2", "member3", "member4"];
team_names.forEach((member) => {
  r_e("members").innerHTML += `<option value="${member}"></option>`;
});
let roles = ["PM", "PE", "PEx", "Sup", "PC"];

// add team members
let num_members = 2;
r_e("rm_team_mem").addEventListener("click", () => {
  if (num_members > 1) {
    r_e(`team_mem_${num_members}`).classList.add("is-hidden");
    r_e(`team_mem_${num_members}_lab`).classList.add("is-hidden");
    r_e(`team_mem_${num_members}_role_lab`).classList.add("is-hidden");
    r_e(`team_mem_${num_members}_role`).classList.add("is-hidden");
    num_members -= 1;
  }
});

r_e("add_team_mem").addEventListener("click", () => {
  if (num_members < 10) {
    num_members += 1;
    r_e(`team_mem_${num_members}`).classList.remove("is-hidden");
    r_e(`team_mem_${num_members}_lab`).classList.remove("is-hidden");
    r_e(`team_mem_${num_members}_role`).classList.remove("is-hidden");
    r_e(`team_mem_${num_members}_role_lab`).classList.remove("is-hidden");
  }
});

// post information
r_e("submit_form").addEventListener("click", () => {
  // test for errors
  // clear errors list
  r_e("errors_list").innerHTML = "";
  // test industry for selection
  if (r_e("Industry").value == "empty") {
    r_e("errors_list").innerHTML += "Missing industry, please select one. <br>";
  }
  // test revenue for selection
  if (r_e("Revenue").value == "") {
    r_e("errors_list").innerHTML +=
      "Missing project revenue, please enter one. <br>";
  }
  // test revenue for invalid number
  else if (isNaN(Number(r_e("Revenue").value.replaceAll(",", "")))) {
    r_e("errors_list").innerHTML +=
      "Invalid Project Revenue, enter as described above and try again <br>";
  } else if (Number(r_e("Revenue").value.replaceAll(",", "")) <= 0) {
    r_e("errors_list").innerHTML +=
      "Invalid Project Revenue, must be greater than 0 <br>";
  }
  // test length for selection
  if (r_e("Length").value == "") {
    r_e("errors_list").innerHTML +=
      "Missing project length, please enter one. <br>";
  }
  // test length for invalid number
  else if (isNaN(Number(r_e("Length").value.replaceAll(",", "")))) {
    r_e("errors_list").innerHTML +=
      "Invalid Project Length, enter as described above and try again <br>";
  } else if (Number(r_e("Length").value.replaceAll(",", "")) <= 0) {
    r_e("errors_list").innerHTML +=
      "Invalid Project Length, must be greater than 0 <br>";
  }
  // test contract type for selection
  if (r_e("Contract").value == "empty") {
    r_e("errors_list").innerHTML +=
      "Missing contract type, please select one. <br>";
  }
  // test zip for selection
  if (r_e("Zip").value == "") {
    r_e("errors_list").innerHTML +=
      "Missing project Zip code, please enter one. <br>";
  }
  // test zip for invalid number
  else if (isNaN(Number(r_e("Zip").value))) {
    r_e("errors_list").innerHTML +=
      "Invalid Zip Code, enter 5 digits only and try again. <br>";
  } else if (r_e("Zip").value.length != 5) {
    r_e("errors_list").innerHTML +=
      "Invalid Zip Code, enter 5 digits only and try again. <br>";
  }
  // test team members
  for (let x = 1; x <= num_members; x++) {
    if (
      !team_names.includes(r_e(`team_mem_${x}`).value) &&
      r_e(`team_mem_${x}`).value != ""
    ) {
      r_e(
        "errors_list"
      ).innerHTML += `Team Member ${x} name not found. Check name again or contract administrator to get them added to the database. <br>`;
    } else if (
      r_e(`team_mem_${x}_role`).value == "" &&
      r_e(`team_mem_${x}`).value != ""
    ) {
      r_e(
        "errors_list"
      ).innerHTML += `Missing Team Member ${x}'s role. Enter role above. <br>`;
    } else if (
      !roles.includes(r_e(`team_mem_${x}_role`).value) &&
      r_e(`team_mem_${x}_role`).value != ""
    ) {
      r_e(
        "errors_list"
      ).innerHTML += `Team Member ${x}'s role not available. Select from one of the 5 roles above. <br>`;
    }
  }

  // run calculation
  if (r_e("errors_list").innerHTML != "") {
    r_e("errors_list").innerHTML += "Fix errors above to run calculator <br>";
  } else {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/", true);
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    let body = JSON.stringify({
      industry: r_e("Industry").value,
      revenue: r_e("Revenue").value,
      length: r_e("Length").value,
      contract: r_e("Contract").value,
      zip: r_e("Zip").value,
      name_1: r_e("team_mem_1").value,
      role_1: r_e("team_mem_1_role").value,
      name_2: r_e("team_mem_2").value,
      role_2: r_e("team_mem_2_role").value,
      name_3: r_e("team_mem_3").value,
      role_3: r_e("team_mem_3_role").value,
      name_4: r_e("team_mem_4").value,
      role_4: r_e("team_mem_4_role").value,
      name_5: r_e("team_mem_5").value,
      role_5: r_e("team_mem_5_role").value,
      name_6: r_e("team_mem_6").value,
      role_6: r_e("team_mem_6_role").value,
      name_7: r_e("team_mem_7").value,
      role_7: r_e("team_mem_7_role").value,
      name_8: r_e("team_mem_8").value,
      role_8: r_e("team_mem_8_role").value,
      name_9: r_e("team_mem_9").value,
      role_9: r_e("team_mem_9_role").value,
      name_10: r_e("team_mem_10").value,
      role_10: r_e("team_mem_10_role").value,
    });
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 201) {
        console.log(JSON.parse(xhr.responseText));
      } else {
        console.log(`Error: ${xhr.status}`);
      }
    };
    xhr.send(body);
    xhr.onload = function () {
      answers = JSON.parse(xhr.response);
      if (Object.keys(answers).length == 1) {
        r_e("errors_list").innerHTML += answers.error;
      }
      r_e("overall_val").innerHTML = answers.Overall;
      r_e("industry_val").innerHTML = answers.Industry;
      r_e("revenue_val").innerHTML = answers.Revenue;
      r_e("length_val").innerHTML = answers.Length;
      r_e("contract_val").innerHTML = answers.Contract;
      r_e("average_val").innerHTML = answers.Average;
      r_e("result_val").innerHTML = answers.Result;
    };
  }
});
