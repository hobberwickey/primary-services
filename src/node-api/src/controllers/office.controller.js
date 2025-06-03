import Municipality from "../models/municipality.model.js";
import Election from "../models/election.model.js";
import Official from "../models/official.model.js";
import Office from "../models/office.model.js";
import Seat from "../models/seat.model.js";
import Term from "../models/term.model.js";

import Requirement from "../models/requirement.model.js";
import Deadline from "../models/deadline.model.js";
import Form from "../models/form.model.js";

let officeController = {
  list: async (req, res, next) => {
    let { municipality_name } = req.params;
    let sequelize = Municipality.sequelize;

    let municipality = await Municipality.findOne({
      where: sequelize.where(
        sequelize.fn("lower", sequelize.col("name")),
        sequelize.fn("lower", municipality_name),
      ),
    });

    // Might want a view here
    let offices = await Office.findAll({
      where: { municipality_id: municipality.id, elected: true },
      include: [
        { model: Official, as: "officials" },
        {
          model: Seat,
          as: "seats",
          include: [
            {
              model: Term,
              as: "terms",
              include: [
                {
                  model: Election,
                  as: "elections",

                  include: {
                    model: Requirement,
                    as: "requirements",
                    include: [
                      { model: Deadline, as: "deadline" },
                      { model: Form, as: "form" },
                    ],
                  },
                },
              ],
            },
          ],
        },
      ],
    });

    return res.status(200).json(offices);
  },

  save: async (req, res, next) => {
    let data = req.body;

    let office = Office.prototype.upsertAll(data);

    return res.status(200).json(office);
  },
};

export default officeController;
