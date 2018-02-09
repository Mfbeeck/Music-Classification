class UsersController < ApplicationController
  require 'json'

  def splash

  end

  # def spotify
  #   spotify_user = RSpotify::User.new(request.env['omniauth.auth'])
  #   # Now you can access user's private data, create playlists and much more
  #   redirect_to root_url(email: spotify_user)
  # end

  def new
    # if request.env['omniauth.auth'].nil?
    #   redirect_to root_url, notice: 'You must sign into Spotify first'
    # end
    # @spotify_user = RSpotify::User.new(request.env['omniauth.auth'])
    @user = User.new()
    @@oauth = request.env['omniauth.auth']
  end

  def create
    @user = User.new(user_params)

    if !@@oauth.nil?
      @spot_json = @@oauth.credentials
      @spot_user_info = @@oauth.info
      @user.private_token = @spot_json['token']
      @user.refresh_token = @spot_json['refresh_token']
      @user.spotify_name = @spot_user_info.display_name
      @user.spotify_id = @spot_user_info.id
    end
    # require 'net/http'
    # scopes = 'user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-library-read user-library-modify'
    # redirect_url = 'http://localhost:3000'
    # url_base = "https://accounts.spotify.com/authorize/?client_id=" + ENV['spotify_client_id'] + "&response_type=code&redirect_uri=" + redirect_url + "&scope=" + scopes + "&state=34fFs29kd09"
    # url = URI.parse(url_base)
    # redirect_to url
    # tokens = `python /Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/lib/assets/python_scripts/get_tokens.py #{ENV['spotify_client_id']} #{ENV['spotify_client_secret']}`
    # @user.access_token = spotify_user['token']
    # @user.private_token = tokens[1]

    if @user.save
      user = User.find_by(id: @user.id)
      if user
  	    session[:user_id] = user.id
        if current_user.classif_type == 'library'
          redirect_to class_playlists_path, notice: 'Logged in!'
        else
          playlists = JSON.parse(`python /Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/lib/assets/python_scripts/get_my_playlists.py #{current_user.private_token}`)
          # playlists = JSON.parse(`python /Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/lib/assets/python_scripts/get_my_playlists.py 'BQCzxXtxazQKdb79LJEKvhxxYy2At0KyiSMve_QaCSBRyhTr1_llc-KQFtvtBVQo1ZplrDvxnrsB1lj0KlhOM62wymg7BWI05jbK10VVIMhcG692VWE501jbjScl73D_Amqm20ILkqXZoOSx8NvsKVmJQ5RRC1ke1xwM2gvsk66ucQay-BFOi9jC_dTP8s2PLoHl-Mksg2jTahevSsqw_vJPyjJW1zx5ToPOo2w'`)
          for playlist in playlists
            @play = Playlist.new()
            @play.playlist_name = playlist[0]
            @play.track_count = playlist[1]
            @play.owner = playlist[2]
            @play.owner_id = playlist[3]
            @play.playlist_url = playlist[4]
            @play.playlist_id = playlist[5]
            @play.playlist_artwork = playlist[6]
            @play.collaborative = playlist[7]
            @play.public_bool = playlist[8]
            @play.user_id = current_user.id
            @play.save
          end

          redirect_to selection_path, notice: 'Logged in!'
        end
    else
      redirect_to root_url, notice: 'Nope!'
    end
    else
      redirect_to root_url, notice: 'You must sign into Spotify first'
    end
  end

  def choose_playlists
    if params[:play_id]
      @selected_playlist = Playlist.find_by(playlist_id: params[:play_id])
      @selected_playlist.unclassified = true
      @selected_playlist.save
    end
    unclassified = "#{current_user.playlists.where(unclassified: true)[0].playlist_url}"
    tracks = JSON.parse(`python /Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/lib/assets/python_scripts/get_playlist_tracks.py #{unclassified} #{current_user.private_token}`)
    for track in tracks
      @track = Track.new()
      @track.playlist_name = track[0]
      @track.playlist_id = track[1]
      @track.track = track[2]
      @track.track_id = track[3]
      @track.artist_name = track[4]
      @track.duration = track[5]
      @track.explicit = track[6]
      @track.track_popularity = track[7]
      @track.acousticness = track[8]
      @track.danceability = track[9]
      @track.energy = track[10]
      @track.instrumentalness = track[11]
      @track.key = track[12]
      @track.liveness = track[13]
      @track.loudness = track[14]
      @track.mode = track[15]
      @track.speechiness = track[16]
      @track.tempo = track[17]
      @track.time_signature = track[18]
      @track.valence = track[19]
      @track.artist_id = track[20]
      @track.artist_followers = track[21]
      @track.artist_genre = track[22]
      @track.artist_img = track[23]
      @track.artist_popularity = track[24]
      @track.album = track[25]
      @track.album_popularity = track[26]
      @track.album_id = track[27]
      @track.album_art = track[28]
      @track.album_release_date = track[29]
      @track.release_date_precision = track[30]
      @track.date_added_to_playlist = track[31]
      @track.preview_url = track[32]
      @track.pop = track[33]
      @track.rap = track[34]
      @track.dance_pop = track[35]
      @track.pop_rap = track[36]
      @track.postteen_pop = track[37]
      @track.hip_hop = track[38]
      @track.rock = track[39]
      @track.trap_music = track[40]
      @track.modern_rock = track[41]
      @track.latin = track[42]
      @track.edm = track[43]
      @track.tropical_house = track[44]
      @track.southern_hip_hop = track[45]
      @track.rnb = track[46]
      @track.classic_rock = track[47]
      @track.unclassified = true
      @track.user_id = current_user.id
      @track.save
    end
    redirect_to choose_path
  end

  def unclassified_selection
    @playlists = current_user.playlists.order(playlist_name: :asc)
  end

  def choose_tracks
    @user = current_user
    @playlists = current_user.playlists.where(unclassified: false).order(playlist_name: :asc)
  end

  def get_tracks
    playlist_ids = params['playlist_urls'].join(",")
    tracks = JSON.parse(`python /Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/lib/assets/python_scripts/get_playlist_tracks.py #{playlist_ids} #{current_user.private_token}`)
    for track in tracks
      @track = Track.new()
      @track.playlist_name = track[0]
      @track.playlist_id = track[1]
      @track.track = track[2]
      @track.track_id = track[3]
      @track.artist_name = track[4]
      @track.duration = track[5]
      @track.explicit = track[6]
      @track.track_popularity = track[7]
      @track.acousticness = track[8]
      @track.danceability = track[9]
      @track.energy = track[10]
      @track.instrumentalness = track[11]
      @track.key = track[12]
      @track.liveness = track[13]
      @track.loudness = track[14]
      @track.mode = track[15]
      @track.speechiness = track[16]
      @track.tempo = track[17]
      @track.time_signature = track[18]
      @track.valence = track[19]
      @track.artist_id = track[20]
      @track.artist_followers = track[21]
      @track.artist_genre = track[22]
      @track.artist_img = track[23]
      @track.artist_popularity = track[24]
      @track.album = track[25]
      @track.album_popularity = track[26]
      @track.album_id = track[27]
      @track.album_art = track[28]
      @track.album_release_date = track[29]
      @track.release_date_precision = track[30]
      @track.date_added_to_playlist = track[31]
      @track.preview_url = track[32]
      @track.pop = track[33]
      @track.rap = track[34]
      @track.dance_pop = track[35]
      @track.pop_rap = track[36]
      @track.postteen_pop = track[37]
      @track.hip_hop = track[38]
      @track.rock = track[39]
      @track.trap_music = track[40]
      @track.modern_rock = track[41]
      @track.latin = track[42]
      @track.edm = track[43]
      @track.tropical_house = track[44]
      @track.southern_hip_hop = track[45]
      @track.rnb = track[46]
      @track.classic_rock = track[47]
      @track.user_id = current_user.id
      @track.save
    end
    redirect_to classified_path
  end

  def classified
    @tracks = current_user.tracks
    raise
    @tracks.to_csv
  end

  private

  def user_params
    params.require(:user).permit(:oauth, :classif_type, :spotify_id, :spotify_name, :private_token, :refresh_token, :model, :fit)
  end
end
