schema_string = File.read('../acquisition/db/structure.sql')

schema_array = []

# splits on things like this
# --
# -- Name: decisions fk_rails_59398d744a; Type: FK CONSTRAINT; Schema: public; Owner: -
# --

schema_string.split(/^-+.*/).each do |x|
  x.strip!

  # The regexp is to filter out the SETs at the beginning of the file as well as migration numbers
  next if x.empty? || x == "\n" || x.match?(/^SE/)

  next unless x.match?(/CREATE TABLE public/)

  schema_array << x
end

File.open('schema_list.py', 'w') { |f| f << "SCHEMA_LIST = #{schema_array}" }
