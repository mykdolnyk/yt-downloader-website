const textField = document.getElementById('video_url')
const goButton = document.getElementById('go_button');
const loadingInfo = document.getElementById('loading-info');
const progressBarFill = document.getElementById('progressbar-fill')
const resultInfo = document.getElementById('result-info');

const errorMessage = "<p>Something went wrong! Please double-check if the ID/URL you entered is correct.</p>"

goButton.addEventListener('click', async function () {
    let userInput = textField.value;

    if (userInput == '') {
        return
    }

    let finalQueueVideoUrl = `${requestVideoUrl}?video_url=${userInput}`;

    displayLoadingStart()

    // Queue the video
    try {
        response = await fetch(finalQueueVideoUrl)
        data = await response.json()
        if (!data.success) {
            displayLoadingDone(errorMessage);
            return;
        }
    }
    catch (error) {
        displayLoadingDone(errorMessage);
        return;
    }

    let videoId = data.video_id
    let finalPollVideoUrl = `${pollVideoUrl}?video_id=${videoId}`;

    // Poll for video status updates
    try {
        for (let attempt = 0; attempt < 120; attempt++) {
            response = await fetch(finalPollVideoUrl)
            data = await response.json()
            if (!data.success) {
                displayLoadingDone(errorMessage);
                break
            }
            if (data.status == 'pending') {
                // Update the progressbar and wait
                console.log(parseFloat(progressBarFill.style.width))
                console.log(parseFloat(data.percent))
                if (parseFloat(data.percent) > parseFloat(progressBarFill.style.width)) {
                    progressBarFill.style.width = `${data.percent}%`;
                }
                await new Promise(resolve => setTimeout(resolve, 500));
                continue
            }
            if (data.status == 'complete') {
                finalShowVideoUrl = `${showVideoUrl}?video_url=${data.id}`
                displayLoadingDone(`<p>Here is your video:</p> <a class="button result_url" href="${finalShowVideoUrl}">${data.title}</a>`);
                break
            }
        }
    } catch (error) {
        displayLoadingDone(errorMessage)
        return true
    }
    
    // Fallback in case there is still no response once the polling is over
    if (loadingInfo.style.display != 'none') {
        displayLoadingDone(errorMessage)
    }
});


function displayLoadingDone(newResultInfo) {
    loadingInfo.style.opacity = 0;
    loadingInfo.style.display = 'none';

    resultInfo.style.opacity = 1;
    resultInfo.style.display = 'flex';
    resultInfo.innerHTML = newResultInfo
}

function displayLoadingStart() {
    textField.value = '';
    progressBarFill.style.width = '0%';

    resultInfo.style.opacity = 0;
    resultInfo.style.display = 'none';
    resultInfo.innerHTML = ''

    loadingInfo.style.display = 'flex';
    requestAnimationFrame(() => {
        loadingInfo.style.opacity = 1;
    });
}