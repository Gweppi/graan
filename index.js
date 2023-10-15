import { OpenEO } from "@openeo/js-client";

try {
    const con = await OpenEO.connect("https://openeo.dataspace.copernicus.eu");

    const info = con.capabilities();

    console.log(info);
} catch (error) {
    console.error(error);
}