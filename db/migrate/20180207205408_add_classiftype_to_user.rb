class AddClassiftypeToUser < ActiveRecord::Migration[5.1]
  def change
    add_column :users, :classif_type, :string
  end
end
