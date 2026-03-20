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
  console.log("changed!");
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

let team_names = ['employee_151', 'employee_240', 'employee_230', 'employee_180', 'employee_27', 'employee_98', 'employee_128', 'employee_203', 'employee_100', 'employee_211', 'employee_139', 'employee_216', 'employee_237', 'employee_198', 'employee_113', 'employee_133', 'employee_172', 'employee_184', 'employee_204', 'employee_187', 'employee_102', 'employee_143', 'employee_234', 'employee_202', 'employee_129', 'employee_195', 'employee_53', 'employee_80', 'employee_174', 'employee_170', 'employee_46', 'employee_87', 'employee_245', 'employee_56', 'employee_181', 'employee_132', 'employee_215', 'employee_228', 'employee_171', 'employee_79', 'employee_185', 'employee_149', 'employee_231', 'employee_82', 'employee_75', 'employee_247', 'employee_90', 'employee_157', 'employee_224', 'employee_148', 'employee_147', 'employee_210', 'employee_11', 'employee_191', 'employee_76', 'employee_121', 'employee_221', 'employee_12', 'employee_70', 'employee_227', 'employee_219', 'employee_112', 'employee_250', 'employee_25', 'employee_182', 'employee_155', 'employee_107', 'employee_161', 'employee_58', 'employee_119', 'employee_114', 'employee_173', 'employee_115', 'employee_72', 'employee_177', 'employee_35', 'employee_89', 'employee_153', 'employee_138', 'employee_104', 'employee_251', 'employee_16', 'employee_160', 'employee_206', 'employee_106', 'employee_94', 'employee_243', 'employee_69', 'employee_32', 'employee_84', 'employee_30', 'employee_154', 'employee_51', 'employee_101', 'employee_159', 'employee_178', 'employee_241', 'employee_103', 'employee_47', 'employee_220', 'employee_52', 'employee_108', 'employee_238', 'employee_92', 'employee_118', 'employee_99', 'employee_167', 'employee_183', 'employee_131', 'employee_29', 'employee_8', 'employee_175', 'employee_193', 'employee_62', 'employee_68', 'employee_15', 'employee_209', 'employee_55', 'employee_39', 'employee_42', 'employee_85', 'employee_169', 'employee_239', 'employee_141', 'employee_10', 'employee_93', 'employee_130', 'employee_33', 'employee_165', 'employee_4', 'employee_19', 'employee_122', 'employee_229', 'employee_74', 'employee_18', 'employee_156', 'employee_164', 'employee_192', 'employee_37', 'employee_73', 'employee_140', 'employee_57', 'employee_158', 'employee_137', 'employee_64', 'employee_111', 'employee_194', 'employee_22', 'employee_135', 'employee_117', 'employee_40', 'employee_109', 'employee_223', 'employee_146', 'employee_232', 'employee_199', 'employee_217', 'employee_50', 'employee_60', 'employee_190', 'employee_63', 'employee_6', 'employee_205', 'employee_20', 'employee_17', 'employee_66', 'employee_189', 'employee_36', 'employee_201', 'employee_2', 'employee_168', 'employee_142', 'employee_197', 'employee_95', 'employee_7', 'employee_222', 'employee_3', 'employee_86', 'employee_43', 'employee_248', 'employee_1', 'employee_152', 'employee_242', 'employee_127', 'employee_145', 'employee_233', 'employee_186', 'employee_13', 'employee_67', 'employee_31', 'employee_162', 'employee_236', 'employee_5', 'employee_81', 'employee_23', 'employee_207', 'employee_124', 'employee_21', 'employee_28', 'employee_61', 'employee_218', 'employee_49', 'employee_179', 'employee_126', 'employee_235', 'employee_105', 'employee_125', 'employee_116', 'employee_134', 'employee_225', 'employee_48', 'employee_120', 'employee_91', 'employee_188', 'employee_26', 'employee_163', 'employee_14', 'employee_144', 'employee_212', 'employee_38', 'employee_226', 'employee_136', 'employee_24', 'employee_200', 'employee_88', 'employee_150', 'employee_97', 'employee_244', 'employee_71', 'employee_78', 'employee_45', 'employee_176', 'employee_65', 'employee_196', 'employee_59', 'employee_41', 'employee_9', 'employee_83', 'employee_249', 'employee_246', 'employee_213', 'employee_123', 'employee_110', 'employee_54', 'employee_96', 'employee_77', 'employee_214', 'employee_208', 'employee_44', 'employee_166'];
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
    xhr.open("POST", "/", true); 
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

