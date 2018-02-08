class CreatePlaylists < ActiveRecord::Migration[5.1]
  def change
    create_table :playlists do |t|
      t.string :playlist_name
      t.integer :track_count
      t.string :owner
      t.string :owner_id
      t.string :playlist_url
      t.string :playlist_id
      t.string :playlist_artwork
      t.boolean :collaborative
      t.boolean :public

      t.timestamps
    end
  end
end
