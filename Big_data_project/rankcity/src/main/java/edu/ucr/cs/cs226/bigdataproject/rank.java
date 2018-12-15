package edu.ucr.cs.cs226.bigdataproject;

import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.ForeachFunction;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.MapFunction;
import org.apache.spark.sql.*;
import org.apache.spark.sql.catalyst.encoders.ExpressionEncoder;
import org.apache.spark.sql.catalyst.encoders.RowEncoder;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructType;
import scala.Int;
import scala.Tuple2;

import java.util.ArrayList;
import java.util.List;

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.sum;
import static org.apache.spark.sql.functions.when;

public class rank {
    public static void main(String[] args) throws Exception {
        SparkSession conf = SparkSession
                .builder()
                .appName("Java Spark SQL ranking")
                .config("spark.some.config.option", "some-value")// spark configuration object
                .master("local")
                .getOrCreate();

        Dataset<Row> FileRDD = conf.read().json("fullAttrU.txt");// reading full attribute file
        StructType struct = new StructType();
        struct = struct.add("name", DataTypes.StringType, false);
        struct = struct.add("rank", DataTypes.DoubleType, false);

        ExpressionEncoder<Row> encoder = RowEncoder.apply(struct);
        // map function to calculate cost of living index
        Dataset<Row>city = FileRDD.map((MapFunction<Row,Row>) row -> {
            double cost_of_living=(Double.parseDouble(Double.toString(row.getAs("rent_index")))
                    + Double.parseDouble(Double.toString(row.getAs("groceries_index")))
                    + Double.parseDouble(Double.toString(row.getAs("restaurant_price_index"))));
 
            double rank_index = Math.max(0, (100 + Double.parseDouble(Double.toString(row.getAs("purchasing_power_incl_rent_index"))) / 2.5
                    - (Double.parseDouble(Double.toString(row.getAs("property_price_to_income_ratio"))) * 1.0)
                    + Double.parseDouble(Double.toString(row.getAs("safety_index"))) / 2.0
                    + Double.parseDouble(Double.toString(row.getAs("health_care_index"))) / 2.5
                    - Double.parseDouble(Double.toString(row.getAs("traffic_time_index"))) / 2.0
                    - Double.parseDouble(Double.toString(row.getAs("pollution_index"))) * 2.0 / 3.0
                    + Double.parseDouble(Double.toString(row.getAs("climate_index"))) / 3.0
                    - (cost_of_living / 10)));

            String name = row.getAs("name");
            Row row1 = RowFactory.create(name,rank_index);
            return row1;
        },encoder);

        Dataset<Row> list = FileRDD.join(city,"name");

        list.show();
        Dataset<Row> filter = list.select("name","rank");
        filter.show();

        filter.write().format("csv").save("sparkoutput1");
       

    }
}
