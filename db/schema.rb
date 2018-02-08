# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20180208060304) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "playlists", force: :cascade do |t|
    t.string "playlist_name"
    t.integer "track_count"
    t.string "owner"
    t.string "owner_id"
    t.string "playlist_url"
    t.string "playlist_id"
    t.string "playlist_artwork"
    t.boolean "collaborative"
    t.boolean "public_bool"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "user_id"
    t.index ["user_id"], name: "index_playlists_on_user_id"
  end

  create_table "unclassifiedtracks", force: :cascade do |t|
    t.string "pred_playlist"
    t.string "pred_id"
    t.string "track"
    t.string "track_id"
    t.string "artist_name"
    t.integer "duration"
    t.integer "explicit"
    t.integer "track_popularity"
    t.float "acousticness"
    t.float "danceability"
    t.float "energy"
    t.float "instrumentalness"
    t.integer "key"
    t.float "liveness"
    t.float "loudness"
    t.integer "mode"
    t.float "speechiness"
    t.float "tempo"
    t.integer "time_signature"
    t.float "valence"
    t.string "artist_id"
    t.integer "artist_followers"
    t.string "artist_genre"
    t.string "artist_img"
    t.integer "artist_popularity"
    t.string "album"
    t.integer "album_popularity"
    t.string "album_id"
    t.string "album_art"
    t.string "album_release_date"
    t.string "release_date_precision"
    t.string "date_added_to_playlist"
    t.string "preview_url"
    t.integer "pop"
    t.integer "rap"
    t.integer "dance_pop"
    t.integer "pop_rap"
    t.integer "postteen_pop"
    t.integer "hip_hop"
    t.integer "rock"
    t.integer "trap_music"
    t.integer "modern_rock"
    t.integer "latin"
    t.integer "edm"
    t.integer "tropical_house"
    t.integer "southern_hip_hop"
    t.integer "rnb"
    t.integer "classic_rock"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "users", force: :cascade do |t|
    t.string "spotify_id"
    t.string "spotify_name"
    t.string "private_token"
    t.string "refresh_token"
    t.string "model"
    t.string "fit"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "classif_type"
  end

  add_foreign_key "playlists", "users"
end
