class AddTrainToPlaylists < ActiveRecord::Migration[5.1]
  def change
    add_column :playlists, :unclassified, :boolean, default: false
  end
end
