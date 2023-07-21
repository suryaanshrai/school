let clickcount = 0;
let sidebarbutton=document.querySelector('#sidebar');
sidebarbutton.addEventListener('click', ()=> {
        let menubar=document.querySelector('#menubar');
        if(clickcount == 0) {
            menubar.style.left="0cm";
            clickcount = 1;
        }
        else {
            menubar.style.left="-6cm";
            clickcount=0;
        }  
});

const homebody = "<p>Sainik School Ambikapur is one of the 24 Sainik Schools of India.\
 It is a purely residential school for boys. The medium of instruction is English. \
 Established by Government of India on 1st of September 2008 at Ambikapur. It is affiliated \
 to Central Board of Secondary Education and is a member of Indian Public Schools Conference (IPSC).\
The school prepares boys for entry into the National Defence Academy, Khadakwasla, Pune and for other walks of life.</p>\
<p>The Sainik Schools are a system of schools in India conceived in 1961 by V. K. Krishna Menon, \
the then Defence Minister of India and established by the MoD under the aegis of the School Society\
 to rectify the regional and class imbalance amongst the Officer cadre of the Indian Armed Forces,\
  by preparing students for entry into the National Defence Academy (NDA), Khadakwasla, Pune.</p>";

const historybody = "<p>The first decade after independence was a traumatic one. The wounds of partition,\
 communal holocaust, resettlement of millions of refugees, integration of the five hundred and odd \
 native states, the clamour of linguistic reorganization – these were but a few of the daunting\
  problems. The compulsive hostility of Pakistan, souring of the once friendly ties with China, \
  turbulence in the North-East and a vast coastline highlighted the necessity of a nationally \
  representative, sizeable and well-equipped Army, Navy and Air-Force.</p> <p>Prior to the Government\
   of India Act of 1935 and the acute demands of World War II, the officer cadre of our armed forces\
    was not open to our countrymen. Rare exceptions were granted to the scions of royalty and blue\
     blood. Analysis of then existing officer cadre revealed a disturbing trend. It remained a monopoly\
      of the so-called martial races and regions and alumni of the highly expensive and elitist public\
       schools beyond the reach of all but a few. In short, our defence forces lacked a truly all-India\
        image, character and ethos. The Indian Military Academy was in existence, therefore the setting up\
         of the National Defence Academy (NDA) at Khadakvasla was but a logical step. The high levels of\
          physical, mental and intellectual attainments needed for induction into the officer cadre could\
           not be nurtured in the common schools mainly because of the lack of infrastructural facilities.\
            A laissez-faire policy to leave it to the already existing, posh public schools would have been\
             grossly unfair to the bright young children all over the country, for whom education in a\
              public school was nothing but a dream. All these reasons prompted the then Defence Minister \
              Shri V K Krishna Menon to envisage a chain of Sainik Schools with at least one in each State to\
               serve as feeders to the NDA. Further, they would act as role models and influence other schools\
                by their example and performance towards a paradigm shift in objectives of school education, as\
                 in the pre-independence years and to some extent even today, our education system is \
                 syllabus-examination oriented and not aimed at all-round development and enhancement of competitive skills.</p>";

const aimbody = "The scheme to establish Sainik Schools was introduced in 1961 with the primary aim of preparing boys academically, \
    physically and mentally for entry into the National Defence Academy and other Defence Academies. <p> Inculcating the following OLQs\
    (Officer Like Qualities) is a big part of the training:<ol><p>Factor – I (Planning and Organising):</p><li>Effective Intelligence</li><li>Reasoning Ability</li>\
    <li>Organising Ability</li><li>Power of Expression</li><p>Factor – II (Social Adjustment)</p><li>Social Adaptability</li><li>Co-operation</li><li>Sense of Responsibility\
    </li><p>Factor – III (Social Effectiveness)</p><li>Initiative</li><li>Self Confidence</li><li>Speed of Decision</li><li>Ability to Influence the Group</li>\
    <li>Liveliness</li><p>Factor – IV (Dynamic)</p><li>Determination</li><li>Courage</li><li>Stamina</li></ol>"

const admissionbody = "Admission is made once in a year in Class VI/IX only through ALL INDIA SAINIK SCHOOL ENTRANCE EXAMINATION\
 which is held on the first Sunday of January every year. The Admission Notice will be published in the advertisements in the\
  leading newspapers in the month of September (generally third/fourth week). Applications for admission are available online \
  in the link <a href=\"http://sainikschooladmission.in/index.html\">http://sainikschooladmission.in/index.html</a>.<p>AGE LIMIT</p>\
  <ul><li>For admission to Class VI, boy should not be less than 10 years and more than 12 years on 31 March.</li>\
<li>For admission to Class IX, boy should not be less than 13 years and more than 15 years on 31 March.</li></ul><p>VACANCIES</p>\
The likely number of vacancies this academic year is 95 for Class VI and 08 for Class IX. However, the number can be changed due \
to policy/administrative reasons."

document.querySelectorAll(".links").forEach(link => {
    link.addEventListener('click', ()=> {
        contentbody = document.querySelector("#content-body");
        contentheading = document.querySelector("#heading");
        contentbody.classList.add("fadeaway");
        contentheading.classList.add("fadeaway");
        setTimeout(()=>{
            if (link.name == "home") {
                contentheading.innerHTML = "Welcome!";
                contentbody.innerHTML = homebody;
            }
            else if (link.name == "admission") {
                contentheading.innerHTML = "Admissions";
                contentbody.innerHTML = admissionbody;
            }
            else if (link.name == "aim") {
                contentheading.innerHTML = "Aim and Values";
                contentbody.innerHTML = aimbody;
            }
            else if (link.name == "history") {
                contentheading.innerHTML = "History";
                contentbody.innerHTML = historybody;
            }
            contentbody.classList.remove("fadeaway");
            contentheading.classList.remove("fadeaway");
        }, 1000);
    });
});