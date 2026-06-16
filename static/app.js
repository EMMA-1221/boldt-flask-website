// toggle section visibility
function toggleSection(id) {
  const el = document.querySelector(`#${id}`);
  el.classList.toggle("is-hidden");
}

// build summary table rows from a data object
function buildSummaryRows(data) {
  const labels = {
    "Pri_D": "Primary Dominance",
    "Pri_E": "Primary Extroversion",
    "Pri_P": "Primary Patience",
    "Pri_C": "Primary Conformity",
    "Cons": "Conscientiousness",
    "Env_D": "Env. Adj. Dominance",
    "Env_E": "Env. Adj. Extroversion",
    "Env_P": "Env. Adj. Patience",
    "Env_C": "Env. Adj. Conformity",
    "High_Trait": "High Trait",
    "Low_Trait": "Low Trait",
    "Decision_Style": "Decision Style",
    "Leadership_Style": "Leadership Style",
    "Learning_Style": "Primary Learning Style",
    "Activist": "Activist Score",
    "Reflector": "Reflector Score",
    "Theorist": "Theorist Score",
    "Pragmatist": "Pragmatist Score",
    "Stress_Level": "Stress Level",
    "Energy_Level": "Energy Level",
    "Proactivity_Score": "Proactivity",
    "Self_Monitoring_Score": "Self-Monitoring",
  };
  let html = "";
  for (const [key, label] of Object.entries(labels)) {
    if (data[key] !== undefined) {
      html += `<tr><td><strong>${label}</strong></td><td>${data[key]}</td></tr>`;
    }
  }
  return html;
}

// element grabber
function r_e(id) {
  return document.querySelector(`#${id}`);
}

// hide
function hide() {
  r_e("home_div").classList.add("is-hidden");
  r_e("guidance_div").classList.add("is-hidden");
  r_e("estimator_div").classList.add("is-hidden");
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
  // 每次打开 guidance 页面时，根据当前下拉选项显示对应 section
  r_e("guidance_filter").dispatchEvent(new Event("change"));
});

// estimator button
r_e("estimator_button").addEventListener("click", () => {
  hide();
  r_e("estimator_div").classList.remove("is-hidden");
});

// guidance dropdown
const guidanceSections = [
  "trait_guidance", "guidance_contract_type", "guidance_duration_less",
  "guidance_duration_great", "guidance_personality", "guidance_industry"
];

function showGuidanceSection(id) {
  guidanceSections.forEach(s => r_e(s).classList.add("is-hidden"));
  if (id) r_e(id).classList.remove("is-hidden");
}

r_e("guidance_filter").addEventListener("change", () => {
  const val = r_e("guidance_filter").value;
  if (val === "Trait Guidance")                                              showGuidanceSection("trait_guidance");
  else if (["LS", "T&M", "GMP", "T&M-GMP", "ILPD"].includes(val))         showGuidanceSection("guidance_contract_type");
  else if (val === "less_yr")                                                showGuidanceSection("guidance_duration_less");
  else if (val === "great_yr")                                               showGuidanceSection("guidance_duration_great");
  else if (["Commercial","Industrial","Healthcare","Power","Institutional"].includes(val)) showGuidanceSection("guidance_industry");
  else if (val === "Company_Wide")                                           showGuidanceSection("guidance_personality");
  else                                                                       showGuidanceSection(null);
});

// 页面加载时初始化 guidance sections（全部隐藏，等用户操作）
showGuidanceSection("trait_guidance");


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
  r_e("industry_label").innerHTML = "Industry";
  r_e("contract_label").innerHTML = "Contract Type";
  ["industry_cim","industry_fpm","contract_cim","contract_fpm",
   "pm_cim","pm_fpm","sup_cim","sup_fpm",
   "team_cim","team_fpm","all_cim","all_fpm",
   "cim_result","fpm_result"].forEach(id => {
    r_e(id).innerHTML = "";
  });
  r_e("errors_list").innerHTML = "";
  r_e("summary_section").classList.add("is-hidden");
  r_e("pm_summary_body").innerHTML = "";
  r_e("sup_summary_body").innerHTML = "";
  r_e("team_summary_body").innerHTML = "";
  r_e("pm_details").classList.add("is-hidden");
  r_e("sup_details").classList.add("is-hidden");
  r_e("team_details").classList.add("is-hidden");
});

// team_names injected from Flask
team_names.forEach((member) => {
  r_e("members").innerHTML += `<option value="${member}"></option>`;
});
let roles = ["PM", "PE", "PEx", "Sup", "PC"];

// add/remove team members
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

// submit form
r_e("submit_form").addEventListener("click", () => {
  r_e("errors_list").innerHTML = "";

  if (r_e("Industry").value == "empty") {
    r_e("errors_list").innerHTML += "Missing industry, please select one. <br>";
  }
  if (r_e("Revenue").value == "") {
    r_e("errors_list").innerHTML += "Missing project revenue, please enter one. <br>";
  } else if (isNaN(Number(r_e("Revenue").value.replaceAll(",", "")))) {
    r_e("errors_list").innerHTML += "Invalid Project Revenue, enter as described above and try again <br>";
  } else if (Number(r_e("Revenue").value.replaceAll(",", "")) <= 0) {
    r_e("errors_list").innerHTML += "Invalid Project Revenue, must be greater than 0 <br>";
  }
  if (r_e("Length").value == "") {
    r_e("errors_list").innerHTML += "Missing project length, please enter one. <br>";
  } else if (isNaN(Number(r_e("Length").value.replaceAll(",", "")))) {
    r_e("errors_list").innerHTML += "Invalid Project Length, enter as described above and try again <br>";
  } else if (Number(r_e("Length").value.replaceAll(",", "")) <= 0) {
    r_e("errors_list").innerHTML += "Invalid Project Length, must be greater than 0 <br>";
  }
  if (r_e("Contract").value == "empty") {
    r_e("errors_list").innerHTML += "Missing contract type, please select one. <br>";
  }
  if (r_e("Zip").value == "") {
    r_e("errors_list").innerHTML += "Missing project Zip code, please enter one. <br>";
  } else if (isNaN(Number(r_e("Zip").value))) {
    r_e("errors_list").innerHTML += "Invalid Zip Code, enter 5 digits only and try again. <br>";
  } else if (r_e("Zip").value.length != 5) {
    r_e("errors_list").innerHTML += "Invalid Zip Code, enter 5 digits only and try again. <br>";
  }
  for (let x = 1; x <= num_members; x++) {
    if (!team_names.includes(r_e(`team_mem_${x}`).value) && r_e(`team_mem_${x}`).value != "") {
      r_e("errors_list").innerHTML += `Team Member ${x} name not found. Check name again or contact administrator to get them added to the database. <br>`;
    } else if (r_e(`team_mem_${x}_role`).value == "" && r_e(`team_mem_${x}`).value != "") {
      r_e("errors_list").innerHTML += `Missing Team Member ${x}'s role. Enter role above. <br>`;
    } else if (!roles.includes(r_e(`team_mem_${x}_role`).value) && r_e(`team_mem_${x}_role`).value != "") {
      r_e("errors_list").innerHTML += `Team Member ${x}'s role not available. Select from one of the 5 roles above. <br>`;
    }
  }

  if (r_e("errors_list").innerHTML != "") {
    r_e("errors_list").innerHTML += "Fix errors above to run calculator <br>";
  } else {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/tool", true);
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    let body = JSON.stringify({
      industry: r_e("Industry").value,
      revenue:  r_e("Revenue").value,
      length:   r_e("Length").value,
      contract: r_e("Contract").value,
      zip:      r_e("Zip").value,
      name_1:  r_e("team_mem_1").value,  role_1:  r_e("team_mem_1_role").value,
      name_2:  r_e("team_mem_2").value,  role_2:  r_e("team_mem_2_role").value,
      name_3:  r_e("team_mem_3").value,  role_3:  r_e("team_mem_3_role").value,
      name_4:  r_e("team_mem_4").value,  role_4:  r_e("team_mem_4_role").value,
      name_5:  r_e("team_mem_5").value,  role_5:  r_e("team_mem_5_role").value,
      name_6:  r_e("team_mem_6").value,  role_6:  r_e("team_mem_6_role").value,
      name_7:  r_e("team_mem_7").value,  role_7:  r_e("team_mem_7_role").value,
      name_8:  r_e("team_mem_8").value,  role_8:  r_e("team_mem_8_role").value,
      name_9:  r_e("team_mem_9").value,  role_9:  r_e("team_mem_9_role").value,
      name_10: r_e("team_mem_10").value, role_10: r_e("team_mem_10_role").value,
    });

    xhr.onload = function () {
      let answers = JSON.parse(xhr.response);
      if (answers.error) {
        r_e("errors_list").innerHTML += answers.error;
        return;
      }
      r_e("industry_label").innerHTML = r_e("Industry").options[r_e("Industry").selectedIndex].text;
      r_e("contract_label").innerHTML = r_e("Contract").options[r_e("Contract").selectedIndex].text;
      r_e("industry_cim").innerHTML = answers.industry_cim;
      r_e("industry_fpm").innerHTML = answers.industry_fpm;
      r_e("contract_cim").innerHTML = answers.contract_cim;
      r_e("contract_fpm").innerHTML = answers.contract_fpm;
      r_e("pm_cim").innerHTML       = answers.pm_cim;
      r_e("pm_fpm").innerHTML       = answers.pm_fpm;
      r_e("sup_cim").innerHTML      = answers.sup_cim;
      r_e("sup_fpm").innerHTML      = answers.sup_fpm;
      r_e("team_cim").innerHTML     = answers.team_cim;
      r_e("team_fpm").innerHTML     = answers.team_fpm;
      r_e("all_cim").innerHTML      = answers.all_cim;
      r_e("all_fpm").innerHTML      = answers.all_fpm;
      r_e("cim_result").innerHTML   = answers.cim_result;
      r_e("fpm_result").innerHTML   = answers.fpm_result;

      // summary section
      r_e("summary_section").classList.remove("is-hidden");

      if (answers.pm_summary) {
        r_e("pm_summary_div").classList.remove("is-hidden");
        r_e("pm_summary_body").innerHTML = buildSummaryRows(answers.pm_summary);
      } else {
        r_e("pm_summary_div").classList.add("is-hidden");
      }

      if (answers.sup_summary) {
        r_e("sup_summary_div").classList.remove("is-hidden");
        r_e("sup_summary_body").innerHTML = buildSummaryRows(answers.sup_summary);
      } else {
        r_e("sup_summary_div").classList.add("is-hidden");
      }

      r_e("team_summary_body").innerHTML = buildSummaryRows(answers.team_summary);
    };

    xhr.send(body);
  }
});
