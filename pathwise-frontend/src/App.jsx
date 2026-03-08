import { useState, useRef } from "react";

function App() {

const [text,setText] = useState("")
const [result,setResult] = useState(null)

const [recording,setRecording] = useState(false)
const [audioBlob,setAudioBlob] = useState(null)
const [recordingStatus,setRecordingStatus] = useState("Idle")

const mediaRecorderRef = useRef(null)
const chunksRef = useRef([])


// ---------------- TEXT ANALYSIS ----------------
const analyzeCareer = async () => {

try{

const response = await fetch("http://35.154.116.53:8000/analyze",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({text:text})
})

const data = await response.json()
setResult(data)

}catch(error){

alert("Server error. Please try again.")

}

}


// ---------------- START RECORDING ----------------
const startRecording = async () => {

try{

const stream = await navigator.mediaDevices.getUserMedia({ audio:true })

const recorder = new MediaRecorder(stream,{ mimeType:"audio/webm" })

chunksRef.current = []

recorder.ondataavailable = (event)=>{
if(event.data.size > 0){
chunksRef.current.push(event.data)
}
}

recorder.onstop = ()=>{

const blob = new Blob(chunksRef.current,{type:"audio/webm"})

setAudioBlob(blob)

setRecordingStatus("Recording stopped")

stream.getTracks().forEach(track=>track.stop())

}

recorder.start(250)

mediaRecorderRef.current = recorder

setRecording(true)
setRecordingStatus("Recording...")

}catch(error){

console.error(error)
alert("Microphone permission denied")

}

}


// ---------------- STOP RECORDING ----------------
const stopRecording = ()=>{

const recorder = mediaRecorderRef.current

if(recorder && recorder.state !== "inactive"){

recorder.stop()
setRecording(false)

}

}


// ---------------- SEND AUDIO ----------------
const submitVoice = async ()=>{

if(!audioBlob){
alert("Please record audio first")
return
}

const formData = new FormData()
formData.append("audio",audioBlob,"recording.webm")

try{

const response = await fetch("http://35.154.116.53:8000/voice-analyze",{
method:"POST",
body:formData
})

const data = await response.json()

setResult(data)

}catch(error){

console.error(error)
alert("Voice analysis failed")

}

}


// ---------------- SAVE RESULT ----------------
const saveResult = async ()=>{

if(!result){
alert("No result to save")
return
}

try{

await fetch("http://35.154.116.53:8000/save",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({

summary: result.ai_summary,

degree: result.profile?.degree,
state: result.profile?.state,
marks: result.profile?.marks,

career: result.career_matches?.[0]?.career,
feasibility_score: result.career_matches?.[0]?.feasibility_score

})
})

alert("Result saved successfully")

}catch(error){

console.error(error)
alert("Failed to save")

}

}


// ---------------- UI ----------------
return(

<div style={{
padding:"40px",
fontFamily:"Arial",
maxWidth:"900px",
margin:"auto"
}}>

<h1>PathWise AI Career Advisor</h1>

<h3>Enter Skills / Resume</h3>

<textarea
rows="6"
style={{width:"100%",padding:"10px"}}
placeholder="Example: I know Python, SQL and I like data analysis..."
value={text}
onChange={(e)=>setText(e.target.value)}
/>

<br/><br/>

<button
onClick={analyzeCareer}
style={{
padding:"12px 20px",
fontSize:"16px",
cursor:"pointer",
background:"#4CAF50",
color:"white",
border:"none",
borderRadius:"6px"
}}
>
Analyze Career
</button>


<hr style={{margin:"40px 0"}}/>


<h2>Voice Input</h2>

<p>Hold the mic button and speak</p>

<button
onPointerDown={startRecording}
onPointerUp={stopRecording}
style={{
fontSize:"20px",
padding:"14px 30px",
cursor:"pointer",
borderRadius:"8px",
border:"none",
background: recording ? "#ff4d4d" : "#007bff",
color:"white"
}}
>

{recording ? "🎙 Recording..." : "🎤 Hold To Speak"}

</button>

<br/><br/>

<p><b>Status:</b> {recordingStatus}</p>

<br/>

<button
onClick={submitVoice}
style={{
padding:"10px 20px",
fontSize:"16px",
cursor:"pointer",
background:"#333",
color:"white",
border:"none",
borderRadius:"6px"
}}
>
Submit Voice
</button>


<hr style={{margin:"40px 0"}}/>


<h2>Results</h2>


{/* PROFILE */}
{result?.profile && (

<div style={{marginBottom:"20px"}}>

<h3>Detected Profile</h3>

<p><b>Degree:</b> {result.profile.degree || "Not detected"}</p>
<p><b>State:</b> {result.profile.state || "Not detected"}</p>
<p><b>Marks:</b> {result.profile.marks || "Not detected"}</p>

</div>

)}


{/* WARNINGS */}
{result?.warnings?.length > 0 && (

<div style={{
background:"#fff3cd",
padding:"12px",
borderRadius:"6px",
marginBottom:"20px"
}}>

<h3>Warnings</h3>

<ul>
{result.warnings.map((w,i)=>(
<li key={i}>{w}</li>
))}
</ul>

</div>

)}


{/* AI SUMMARY */}
{result?.career_matches && (

<div>

<h3>AI Summary</h3>
<p>{result.ai_summary}</p>

<h3>AI Advice</h3>
<p>{result.ai_advice}</p>


{/* ELIGIBLE SCHOLARSHIPS */}
{result?.eligibility?.eligible_schemes?.length > 0 && (

<div>

<h3>Eligible Scholarships</h3>

{result.eligibility.eligible_schemes.map((item,index)=>(

<div key={index} style={{
border:"1px solid #ddd",
padding:"15px",
marginBottom:"10px",
borderRadius:"8px"
}}>

<p><b>Scheme:</b> {item.scheme}</p>

<p><b>Status:</b> Eligible</p>

</div>

))}

</div>

)}


{/* NEAR ELIGIBLE */}
{result?.eligibility?.near_eligible_schemes?.length > 0 && (

<div>

<h3>Almost Eligible Scholarships</h3>

{result.eligibility.near_eligible_schemes.map((item,index)=>(

<div key={index} style={{
border:"1px solid #ddd",
padding:"15px",
marginBottom:"10px",
borderRadius:"8px",
background:"#fff8e1"
}}>

<p><b>Scheme:</b> {item.scheme}</p>

<p><b>Reason:</b> {item.reasons?.join(", ")}</p>

</div>

))}

</div>

)}


{/* CAREERS */}
<h3>Recommended Careers</h3>

{result.career_matches.map((career,index)=>(

<div key={index} style={{
border:"1px solid #ddd",
padding:"20px",
marginBottom:"20px",
borderRadius:"10px",
background:"#f9f9f9"
}}>

<h3>{career.career}</h3>

<p><b>Feasibility Score:</b> {career.feasibility_score}</p>

<p><b>Matched Skills:</b> {career.matched_skills?.join(", ")}</p>

<p><b>Missing Skills:</b> {career.missing_skills?.join(", ")}</p>

<h4>Roadmap</h4>

<ul>
{career?.roadmap?.steps?.map((step,i)=>(
<li key={i}>{step.action}</li>
))}
</ul>

</div>

))}

{/* SAVE BUTTON */}

<button
onClick={saveResult}
style={{
padding:"12px 25px",
background:"#28a745",
color:"white",
border:"none",
borderRadius:"8px",
fontSize:"16px",
cursor:"pointer"
}}
>
Save Result
</button>

</div>

)}

</div>

)

}

export default App