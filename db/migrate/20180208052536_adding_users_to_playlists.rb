class AddingUsersToPlaylists < ActiveRecord::Migration[5.1]
  def change
    add_reference :playlists, :user, index: true
    add_foreign_key :playlists, :users
    add_reference :tracks, :user, index: true
    add_foreign_key :tracks, :users
  end
end
