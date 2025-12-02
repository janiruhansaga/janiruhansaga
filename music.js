/* music.js - All-in-One Music Player Script */

document.addEventListener("DOMContentLoaded", function () {
    // 1. සින්දුවේ නම මෙතනට දෙන්න (ෆෝල්ඩර් එකේ තියෙන නමම වෙන්න ඕන)
    const musicFile = "music.mp3"; 

    // --- HTML බට්න් එක සහ CSS ඔටෝම ඇඩ් කරන කොටස ---
    const style = document.createElement('style');
    style.innerHTML = `
        .music-btn-fixed {
            position: fixed;
            bottom: 20px;
            right: 20px; /* දකුණු පැත්තේ යට */
            width: 50px;
            height: 50px;
            background-color: #00ccff; /* බට්න් එකේ පාට */
            border-radius: 50%;
            border: none;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(0, 204, 255, 0.4);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999; /* හැම එකටම උඩින් */
            transition: transform 0.3s, background-color 0.3s;
        }
        .music-btn-fixed:hover {
            transform: scale(1.1);
            background-color: #fff;
        }
        .music-btn-fixed i {
            font-size: 20px;
            color: #000;
        }
        .music-pulse {
            animation: pulse-animation 2s infinite;
        }
        @keyframes pulse-animation {
            0% { box-shadow: 0 0 0 0 rgba(0, 204, 255, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(0, 204, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 204, 255, 0); }
        }
    `;
    document.head.appendChild(style);

    // බට්න් එක හදමු
    const btn = document.createElement('button');
    btn.className = "music-btn-fixed";
    btn.id = "globalMusicBtn";
    btn.innerHTML = '<i class="fa-solid fa-music"></i>'; // අයිකන් එක
    document.body.appendChild(btn);

    // Audio Player එක හදමු
    const audio = new Audio(musicFile);
    audio.loop = true; // දිගටම Play වෙන්න
    audio.volume = 0.5; // සද්දේ 50%

    // --- Logic කොටස (මතක තියාගන්න සිස්ටම් එක) ---
    
    // කලින් ON කරලද තිබ්බේ?
    let isPlaying = localStorage.getItem('musicPlaying') === 'true';
    // කලින් කොතනද නතර වුනේ? (Time)
    let savedTime = parseFloat(localStorage.getItem('musicTime')) || 0;

    // අයිකන් එක අප්ඩේට් කරන function එක
    function updateIcon() {
        if (isPlaying) {
            btn.innerHTML = '<i class="fa-solid fa-music"></i>';
            btn.classList.add('music-pulse');
        } else {
            btn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
            btn.classList.remove('music-pulse');
        }
    }

    // සින්දුව Play/Pause කරන function එක
    function togglePlay() {
        if (isPlaying) {
            audio.pause();
            isPlaying = false;
        } else {
            audio.play().catch(e => console.log("User interaction needed"));
            isPlaying = true;
        }
        updateIcon();
        // ස්ටේටස් එක බ්‍රව්සර් එකේ සේව් කරගන්නවා
        localStorage.setItem('musicPlaying', isPlaying);
    }

    // පිටුව ලෝඩ් වෙද්දී Play කරන්න ට්‍රයි කරනවා
    if (isPlaying) {
        audio.currentTime = savedTime; // කලින් නැවැත්තුන තැනින් පටන් ගන්න
        updateIcon();
        const playPromise = audio.play();
        
        if (playPromise !== undefined) {
            playPromise.catch(error => {
                // Browser එකෙන් Block කළොත්, Click එකක් බලාපොරොත්තු වෙනවා
                console.log("Autoplay blocked. Waiting for click.");
                isPlaying = false;
                updateIcon();
                // එක පාරක් Click කරපු ගමන් Play වෙන්න හදනවා
                document.body.addEventListener('click', function startOnce() {
                    audio.play();
                    isPlaying = true;
                    updateIcon();
                    localStorage.setItem('musicPlaying', 'true');
                    document.body.removeEventListener('click', startOnce);
                }, { once: true });
            });
        }
    } else {
        updateIcon(); // Off නම් Off විදියට පෙන්නන්න
    }

    // බට්න් එක Click කළාම
    btn.addEventListener('click', togglePlay);

    // වෙන පිටුවකට යන්න කලින් දැනට සින්දුව යන Time එක සේව් කරගන්නවා
    window.addEventListener('beforeunload', function () {
        localStorage.setItem('musicTime', audio.currentTime);
    });
});