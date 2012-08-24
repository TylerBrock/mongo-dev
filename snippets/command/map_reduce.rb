mapper = "function(){
  this.tags.forEach(
    function(z){
      emit( z , { count : 1 } );
    }
  );
};"

reducer = "function( key , values ){
  var total = 0;
  for ( var i=0; i<values.length; i++ )
    total += values[i].count;
    return { count : total };
};"

collection.map_reduce(mapper, reducer)
