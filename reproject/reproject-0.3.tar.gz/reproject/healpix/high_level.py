from .core import healpix_to_image, image_to_healpix
from .utils import parse_input_healpix_data, parse_coord_system
from ..utils import parse_input_data, parse_output_projection

__all__ = ['reproject_from_healpix', 'reproject_to_healpix']


def reproject_from_healpix(input_data, output_projection, shape_out=None, hdu_in=None, order='bilinear', nested=False, field=0):
    """
    Reproject data from a HEALPIX projection to a standard projection.

    .. note:: This function uses healpy, which is licensed
              under the GPLv2, so any package using this funtions has to (for
              now) abide with the GPLv2 rather than the BSD license.

    Parameters
    ----------
    input_data : str or `~astropy.io.fits.TableHDU` or `~astropy.io.fits.BinTableHDU` or tuple
        The input data to reproject. This can be:

            * The name of a HEALPIX FITS file
            * A `~astropy.io.fits.TableHDU` or `~astropy.io.fits.BinTableHDU`
              instance
            * A tuple where the first element is a `~numpy.ndarray` and the
              second element is a `~astropy.coordinates.BaseCoordinateFrame`
              instance or a string alias for a coordinate frame.

    output_projection : `~astropy.wcs.WCS` or `~astropy.io.fits.Header`
        The output projection, which can be either a `~astropy.wcs.WCS`
        or a `~astropy.io.fits.Header` instance.
    shape_out : tuple, optional
        If ``output_projection`` is a `~astropy.wcs.WCS` instance, the
        shape of the output data should be specified separately.
    hdu_in : int or str, optional
        If ``input_data`` is a FITS file, specifies the HDU to use.
    order : int or str, optional
        The order of the interpolation (if ``mode`` is set to
        ``'interpolation'``). This can be either one of the following strings:

            * 'nearest-neighbor'
            * 'bilinear'

        or an integer. A value of ``0`` indicates nearest neighbor
        interpolation.
    nested : bool, optional
        The order of the healpix_data, either nested (True) or ring (False)
    field : int, optional
        The column to read from the HEALPIX FITS file. If the fits file is a
        partial-sky file, field=0 corresponds to the first column after the
        pixel index column.

    Returns
    -------
    array_new : `~numpy.ndarray`
        The reprojected array
    footprint : `~numpy.ndarray`
        Footprint of the input array in the output array. Values of 0 indicate
        no coverage or valid values in the input image, while values of 1
        indicate valid values.
    """

    array_in, coord_system_in = parse_input_healpix_data(input_data, hdu_in=hdu_in, field=field)
    wcs_out, shape_out = parse_output_projection(output_projection, shape_out=shape_out)

    return healpix_to_image(array_in, coord_system_in, wcs_out, shape_out, order=order, nested=nested)


def reproject_to_healpix(input_data, coord_system_out, hdu_in=None, order='bilinear', nested=False, nside=128):
    """
    Reproject data from a standard projection to a HEALPIX projection.

    .. note:: This function uses healpy, which is licensed
              under the GPLv2, so any package using this funtions has to (for
              now) abide with the GPLv2 rather than the BSD license.

    Parameters
    ----------
    input_data : str or `~astropy.io.fits.HDUList` or `~astropy.io.fits.PrimaryHDU` or `~astropy.io.fits.ImageHDU` or tuple
        The input data to reproject. This can be:

            * The name of a FITS file
            * An `~astropy.io.fits.HDUList` object
            * An image HDU object such as a `~astropy.io.fits.PrimaryHDU` or
              `~astropy.io.fits.ImageHDU` instance
            * A tuple where the first element is a `~numpy.ndarray` and the
              second element is either a `~astropy.wcs.WCS` or a
              `~astropy.io.fits.Header` object

    coord_system_out : `~astropy.coordinates.BaseCoordinateFrame` or str
        The output coordinate system for the HEALPIX projection
    hdu_in : int or str, optional
        If ``input_data`` is a FITS file or an `~astropy.io.fits.HDUList`
        instance, specifies the HDU to use.
    order : int or str, optional
        The order of the interpolation (if ``mode`` is set to
        ``'interpolation'``). This can be either one of the following strings:

            * 'nearest-neighbor'
            * 'bilinear'
            * 'biquadratic'
            * 'bicubic'

        or an integer. A value of ``0`` indicates nearest neighbor
        interpolation.
    nested : bool
        The order of the healpix_data, either nested (True) or ring (False)
    nside : int, optional
        The resolution of the HEALPIX projection.

    Returns
    -------
    array_new : `~numpy.ndarray`
        The reprojected array
    footprint : `~numpy.ndarray`
        Footprint of the input array in the output array. Values of 0 indicate
        no coverage or valid values in the input image, while values of 1
        indicate valid values.
    """

    array_in, wcs_in = parse_input_data(input_data, hdu_in=hdu_in)
    coord_system_out = parse_coord_system(coord_system_out)

    if wcs_in.has_celestial and wcs_in.naxis == 2:
        return image_to_healpix(array_in, wcs_in, coord_system_out, nside=nside, order=order, nested=nested)
    else:
        raise NotImplementedError("Only data with a 2-d celestial WCS can be reprojected to a HEALPIX projection")
