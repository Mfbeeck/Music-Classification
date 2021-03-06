class Track < ApplicationRecord
  require 'csv'

  def self.to_csv
    attributes = self.column_names

    CSV.generate(headers: true) do |csv|
      csv << attributes

      all.each do |track|
        csv << attributes.map{ |attr| track.send(attr) }
      end
    end
  end

  # def name
  #   "#{first_name} #{last_name}"
  # end

end
