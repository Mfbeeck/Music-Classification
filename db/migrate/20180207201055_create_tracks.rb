class CreateTracks < ActiveRecord::Migration[5.1]
  def change
    create_table :tracks do |t|
      t.string :pred_playlist
      t.string :pred_id
      t.string :pred_proba
      t.string :playlist_name
      t.string :playlist_id
      t.string :track
      t.string :track_id
      t.string :artist_name
      t.integer :duration
      t.integer :explicit
      t.integer :track_popularity
      t.float :acousticness
      t.float :danceability
      t.float :energy
      t.float :instrumentalness
      t.integer :key
      t.float :liveness
      t.float :loudness
      t.integer :mode
      t.float :speechiness
      t.float :tempo
      t.integer :time_signature
      t.float :valence
      t.string :artist_id
      t.integer :artist_followers
      t.string :artist_genre
      t.string :artist_img
      t.integer :artist_popularity
      t.string :album
      t.integer :album_popularity
      t.string :album_id
      t.string :album_art
      t.string :album_release_date
      t.string :release_date_precision
      t.string :date_added_to_playlist
      t.string :preview_url
      t.integer :pop
      t.integer :rap
      t.integer :rap
      t.integer :dance_pop
      t.integer :pop_rap
      t.integer :postteen_pop
      t.integer :hip_hop
      t.integer :rock
      t.integer :trap_music
      t.integer :modern_rock
      t.integer :latin
      t.integer :edm
      t.integer :tropical_house
      t.integer :southern_hip_hop
      t.integer :rnb
      t.integer :classic_rock
      t.boolean :unclassified, default: false
      t.timestamps
    end
  end
end
