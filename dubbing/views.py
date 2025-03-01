from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .forms import VideoUploadForm
import os
from .video_dubbing_logic import process_video  # This will be the logic extracted from your notebook

def video_upload(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video']

            # Save the uploaded video file
            video_path = os.path.join('media/', video_file.name)
            with open(video_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # Get the selected target language from the form
            target_language = form.cleaned_data['language']
            print(f"Selected language: {target_language}")

            # Process the video with dubbing logic and selected language
            dubbed_video_path = process_video(video_path, target_language)  # Pass the language argument

            # Provide the dubbed video for download
            response = FileResponse(open(dubbed_video_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(dubbed_video_path)}"'
            return response
    else:
        form = VideoUploadForm()
    
    return render(request, 'dubbing/upload.html', {'form': form})

def video_download(request, filename):
    file_path = f'media/{filename}'  # Assuming files are stored in a 'media' folder
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

